from api.v1.mixins import CreatedAtRangeFilterMixin


class UserFiltersIn(CreatedAtRangeFilterMixin, extra='forbid'):
    search: str | None = None
    is_active: bool | None = None
