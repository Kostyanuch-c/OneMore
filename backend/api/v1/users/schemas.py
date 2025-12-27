from datetime import datetime

from ninja import Schema

from apps.users.entities import UserEntity


class UserOutSchema(Schema):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    username: str
    created_at: datetime

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserOutSchema':
        return UserOutSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.full_name,
            username=entity.username,
            created_at=entity.created_at,
        )
