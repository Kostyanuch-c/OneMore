from apps.users.entities import UserEntity
from apps.users.models import User


class UserConverter:
    @staticmethod
    def to_entity(model: User) -> UserEntity:
        return UserEntity(
            id=model.pk,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            full_name=model.full_name,
            created_at=model.date_joined,
        )
