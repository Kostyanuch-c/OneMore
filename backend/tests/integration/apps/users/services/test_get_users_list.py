from django.db.models import Q

import pytest

from apps.users.entities import UserEntity
from apps.users.filters import UserFilters


@pytest.mark.parametrize(
    ('filters', 'expected_count', 'limit', 'offset'),
    [
        (UserFilters(), 10, 10, 0),
        (UserFilters(), 2, 2, 1),
        (UserFilters(is_active=True), 1, 1, 0),
        (UserFilters(is_active=False), 2, 2, 0),
    ],
)
def test_get_users_list_returns_users_with_filters_pagination_and_default_sort(
    user_service,
    user_factory,
    user_model,
    limit,
    offset,
    filters,
    expected_count,
):
    user_factory.create_batch(5)
    user_factory.create_batch(10, is_active=False)

    users_entity = user_service.get_users_list(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    assert all(isinstance(user, UserEntity) for user in users_entity)
    assert len(users_entity) == expected_count
    assert user_model.objects.count() == 15  # noqa

    q_filters = Q()
    if filters.is_active is not None:
        q_filters &= Q(is_active=filters.is_active)

    db_users = (
        user_model.objects.filter(q_filters)
        .order_by('-date_joined')
        .all()[offset : offset + limit]
    )

    assert [user.id for user in users_entity] == [user.id for user in db_users]
