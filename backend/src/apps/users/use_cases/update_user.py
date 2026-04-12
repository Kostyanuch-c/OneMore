from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.users.dto import UserUpdateDTO
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class UpdateUser(BaseUseCase[UserEntity]):
    service: UserService
    user_id: int
    user_data: UserUpdateDTO

    def act(self) -> UserEntity:
        return self.service.update_user(
            user_id=self.user_id,
            user_data=self.user_data,
        )
