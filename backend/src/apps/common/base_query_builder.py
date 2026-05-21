from typing import Any

from django.db.models import Q


class BaseQueryBuilder[TFilters]:
    FILTER_LOOKUPS: dict[str, str] = {}
    SEARCH_FIELDS: tuple[str, ...] = ()

    def build(self, filters: TFilters, base_query: Q | None = None) -> Q:
        query = base_query if base_query is not None else self.default_query()

        query &= self.build_search_query(filters)
        query &= self.build_mapped_filters_query(filters)

        return query

    def default_query(self) -> Q:
        # Override this method in the child if needed some filters are always applied
        return Q()

    def build_search_query(self, filters: TFilters) -> Q:
        search = getattr(filters, 'search', None)

        if not search:
            return Q()

        query = Q()

        for field in self.SEARCH_FIELDS:
            query |= Q(**{f'{field}__icontains': search})

        return query

    def build_mapped_filters_query(self, filters: TFilters) -> Q:
        query = Q()

        for field_name, orm_lookup in self.FILTER_LOOKUPS.items():
            value = getattr(filters, field_name, None)

            if self._is_empty(value):
                continue

            query &= Q(**{orm_lookup: value})

        return query

    def _is_empty(self, value: Any) -> bool:
        # We need this method because False is a valid value for some filters
        return value is None or value in ('', (), [])
