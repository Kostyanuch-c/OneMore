from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserFilters:
    search: str | None = None
    is_active: bool = True

    created_from: datetime | None = None
    created_to: datetime | None = None
