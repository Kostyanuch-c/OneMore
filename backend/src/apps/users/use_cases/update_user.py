from collections.abc import Callable
from dataclasses import dataclass

from django.conf import settings
from django.db import transaction

from apps.common import BaseUseCase
from apps.users.dto import UserUpdateDTO
from apps.users.entities import UserEntity
from apps.users.exceptions.users import ReservedUserNameError
from apps.users.services import UserService


@dataclass
class UpdateUser(BaseUseCase[UserEntity]):
    service: UserService
    user_id: int
    user_data: UserUpdateDTO

    def act(self) -> UserEntity:
        with transaction.atomic():
            return self.service.update_user(
                user_id=self.user_id,
                user_data=self.user_data,
            )

    def get_validators(self) -> list[Callable[[], None]]:
        return [
            self.validate_username,
        ]

    def validate_username(self) -> None:
        if (
            self.user_data.username
            and self.user_data.username.lower() in settings.RESERVED_USERNAMES
        ):
            raise ReservedUserNameError
