from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    full_name: str | None
    email: str | None
    role: str
    created_at: datetime
