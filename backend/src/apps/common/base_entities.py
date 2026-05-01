from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BaseEntity:
    id: int
    created_at: datetime
    updated_at: datetime


@dataclass
class Page[TEntity]:
    items: list[TEntity]
    total: int
