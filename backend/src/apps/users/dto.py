from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserFilters:
    search: str | None = None
    is_active: bool | None = None

    created_from: datetime | None = None
    created_to: datetime | None = None


@dataclass(frozen=True)
class UserUpdateDTO:
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    def to_update_dict(self) -> dict[str, object]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }
