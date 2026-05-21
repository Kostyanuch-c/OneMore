from dataclasses import dataclass

from django.db.models import Q

import pytest

from apps.common.base_query_builder import BaseQueryBuilder


@dataclass
class QueryBuilderTestFilters:
    search: str | None = None
    is_active: bool | None = None
    created_from: object | None = None
    ids: tuple[int, ...] = ()


class QueryBuilderForTests(BaseQueryBuilder[QueryBuilderTestFilters]):
    FILTER_LOOKUPS = {
        'is_active': 'is_active',
        'created_from': 'created_at__gte',
        'ids': 'id__in',
    }

    SEARCH_FIELDS = (
        'title',
        'description',
    )


@pytest.mark.parametrize(
    ('filters', 'expected_query'),
    [
        (
            QueryBuilderTestFilters(),
            Q(),
        ),
        (
            QueryBuilderTestFilters(is_active=False),
            Q(is_active=False),
        ),
        (
            QueryBuilderTestFilters(search='john'),
            Q(title__icontains='john') | Q(description__icontains='john'),
        ),
        (
            QueryBuilderTestFilters(created_from='2024-01-01'),
            Q(created_at__gte='2024-01-01'),
        ),
        (
            QueryBuilderTestFilters(ids=(1, 2, 3)),
            Q(id__in=(1, 2, 3)),
        ),
        (
            QueryBuilderTestFilters(
                search='john',
                is_active=True,
                created_from='2024-01-01',
                ids=(1, 2, 3),
            ),
            (Q(title__icontains='john') | Q(description__icontains='john'))
            & Q(is_active=True)
            & Q(created_at__gte='2024-01-01')
            & Q(id__in=(1, 2, 3)),
        ),
    ],
)
def test_base_query_builder_builds_query(filters, expected_query):
    result = QueryBuilderForTests().build(filters)

    assert result == expected_query


def test_base_query_builder_skips_empty_values_but_not_false():
    filters = QueryBuilderTestFilters(
        search='',
        is_active=False,
        ids=(),
    )

    result = QueryBuilderForTests().build(filters)

    assert result == Q(is_active=False)


def test_base_query_builder_applies_base_query():
    filters = QueryBuilderTestFilters(is_active=True)
    base_query = Q(role='admin')

    result = QueryBuilderForTests().build(
        filters=filters,
        base_query=base_query,
    )

    assert result == Q(role='admin') & Q(is_active=True)
