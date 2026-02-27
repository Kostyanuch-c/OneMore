from datetime import datetime

from ninja import Schema


class UserFiltersIn(Schema):
    search: str | None = None
    is_active: bool = True

    created_from: datetime | None = None
    created_to: datetime | None = None
