from dataclasses import dataclass
from typing import Any

from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class UpdateUser(BaseUseCase):
    service: UserService
    user_id: int
    update_data: dict[str, Any]

    def act(self) -> UserEntity:
        return self.service.update_user(
            user_id=self.user_id,
            user_data=self.update_data,
        )
