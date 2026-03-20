import uuid
from dataclasses import dataclass

from django.utils.functional import cached_property

from api.v1.profile.schemas import UserInputSchema
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class GetOrCreateUser(BaseUseCase):
    service: UserService
    create_data: UserInputSchema

    @cached_property
    def username(self) -> str:
        return self.create_data.email or str(uuid.uuid4())

    def act(self) -> UserEntity:
        existing_user = self.service.get_user_by_email(self.create_data.email)
        if existing_user is not None:
            return existing_user

        return self.service.create_user(
            username=self.username, email=self.create_data.email
        )
