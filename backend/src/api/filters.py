from enum import Enum
from typing import Any

from ninja import Schema

from project.settings import PAGE_LIMIT


class PaginationOut(Schema):
    offset: int
    limit: int
    total: int


class PaginationIn(Schema):
    offset: int = 0
    limit: int = PAGE_LIMIT


class DefaultFilter(Enum):
    NOT_SET: Any
