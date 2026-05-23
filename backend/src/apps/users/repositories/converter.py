from typing import TYPE_CHECKING

from apps.users.entities import UserEntity


if TYPE_CHECKING:
    from apps.users.models import User


class UserConverter:
    @staticmethod
    def to_entity(*, model: User) -> UserEntity:
        return UserEntity(
            id=model.pk,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            full_name=model.full_name,
            email=model.email,
            is_active=model.is_active,
            is_tutor=model.is_tutor,
            is_staff=model.is_staff,
            date_joined=model.date_joined,
        )
