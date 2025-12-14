from datetime import datetime

from ninja import Schema


class UserOutSchema(Schema):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    username: str
    created_at: datetime
