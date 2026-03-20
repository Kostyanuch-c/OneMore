import uuid
from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class GetOrCreateUser(BaseUseCase):
    service: UserService
    email: str

    @property
    def username(self) -> str:
        return f'{self.email.split("@", 1)[0][:50]}_{uuid.uuid4().hex[:12]}'

    def act(self) -> tuple[UserEntity, bool]:
        existing_user = self.service.get_user_by_email(
            email=self.email, include_inactive=True
        )
        if existing_user is not None:
            return existing_user, False

        return (
            self.service.create_user(username=self.username, email=self.email),
            True,
        )
