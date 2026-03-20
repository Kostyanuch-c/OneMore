from enum import Enum
from typing import Any

from pydantic import Field

from ninja import Schema

from django.conf import settings


class PaginationOut(Schema):
    offset: int
    limit: int
    total: int


class PaginationIn(Schema):
    offset: int = Field(0, ge=0)
    limit: int = Field(settings.PAGE_LIMIT, ge=1, le=settings.MAX_PAGE_LIMIT)


class DefaultFilter(Enum):
    NOT_SET: Any
