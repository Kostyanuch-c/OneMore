from datetime import datetime

from pydantic import model_validator

from ninja import Schema

from api.exceptions import InvalidTimeFilterError


class UserFiltersIn(Schema):
    search: str | None = None
    is_active: bool = True

    created_from: datetime | None = None
    created_to: datetime | None = None

    @model_validator(mode='after')
    def validate_time_filter(self) -> UserFiltersIn:
        if self.created_from and self.created_to:  # noqa: SIM102
            if self.created_from > self.created_to:
                raise InvalidTimeFilterError
        return self
