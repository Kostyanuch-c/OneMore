from datetime import datetime
from typing import Self

from pydantic import model_validator

from ninja import Schema

from api.exceptions import InvalidTimeFilterError


class CreatedAtRangeFilterMixin(Schema):
    created_from: datetime | None = None
    created_to: datetime | None = None

    @model_validator(mode='after')
    def validate_created_at_range(self) -> Self:
        if self.created_from and self.created_to:  # noqa: SIM102
            if self.created_from > self.created_to:
                raise InvalidTimeFilterError

        return self
