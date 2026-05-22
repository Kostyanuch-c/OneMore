from datetime import datetime
from typing import Protocol, Self

from pydantic import ConfigDict, model_validator

from ninja import Schema

from api.exceptions import InvalidTimeFilterError


class CreatedAtRangeFilterMixin(Schema):
    model_config = ConfigDict(extra='forbid')

    created_from: datetime | None = None
    created_to: datetime | None = None

    @model_validator(mode='after')
    def validate_created_at_range(self) -> Self:
        if self.created_from and self.created_to:  # noqa: SIM102
            if self.created_from > self.created_to:
                raise InvalidTimeFilterError

        return self


class EnumOption(Protocol):
    @property
    def value(self) -> str: ...

    @property
    def label(self) -> str: ...


class BaseEnumSchema(Schema):
    model_config = ConfigDict(extra='forbid')

    value: str
    label: str

    @classmethod
    def from_option(cls, option: EnumOption) -> Self:
        return cls(
            value=option.value,
            label=option.label,
        )
