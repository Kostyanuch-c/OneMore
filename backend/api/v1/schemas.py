from typing import Any

from ninja import Schema

from pydantic.fields import Field


class ApplicationErrorSchema(Schema):
    message: str
    extra: dict[str, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
