from dataclasses import dataclass

from api.v1.users.schemas import UserUpdateSchema
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class UpdateUser(BaseUseCase):
    service: UserService
    update_data: UserUpdateSchema

    def act(self) -> UserEntity:
        return self.service.update_user(
            user_id=self.update_data.user_id,
            user_data=self.update_data.dict(
                exclude={'user_id'}, exclude_none=True
            ),
        )
