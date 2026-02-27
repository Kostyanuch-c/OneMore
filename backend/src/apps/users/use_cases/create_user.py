from dataclasses import dataclass

from api.v1.users.schemas import UserInputSchema
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class CreateUser(BaseUseCase):
    service: UserService
    create_data: UserInputSchema

    def act(self) -> UserEntity:
        return self.service.create_user(
            username=self.create_data.username,
            email=self.create_data.email,
            password=self.create_data.password,
        )
