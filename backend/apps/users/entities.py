from dataclasses import dataclass
from datetime import datetime

from ninja import Schema


@dataclass
class UserEntity:
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    full_name: str | None
    created_at: datetime


class UserInputSchema(Schema):
    password: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str


class UserUpdateSchema(Schema):
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
