from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class BaseEntity:
    id: int
    created_at: datetime
    updated_at: datetime
