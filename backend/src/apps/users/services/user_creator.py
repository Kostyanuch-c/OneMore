from collections.abc import Callable
from dataclasses import dataclass

from django.core.validators import validate_email
from django.db import IntegrityError

from api.v1.users.schemas import UserInputSchema
from apps.common.base_service import BaseService
from apps.common.utils import (
    conflict,
    constraint_name,
    normalize_email_strict,
)
from apps.users.entities import (
    UserEntity,
)
from apps.users.repositories.user_repository import UserRepository


@dataclass
class UserCreator(BaseService):
    repository = UserRepository()
    create_data: UserInputSchema

    @property
    def normalize_email(self) -> str | None:
        return normalize_email_strict(self.create_data.email)

    def act(self) -> UserEntity:
        try:
            return self.repository.create_user(
                username=self.create_data.username,
                email=self.normalize_email,
                password=self.create_data.password,
            )
        except IntegrityError as e:
            cname = constraint_name(e)

            if cname == self.repository.USERNAME_CONSTRAINT:
                raise conflict('username') from e
            if cname == self.repository.EMAIL_CONSTRAINT:
                raise conflict('email') from e

            raise

    def get_validators(self) -> list[Callable[[], None]]:
        return [
            self.validate_username_unique,
            self.validate_email,
            self.validate_email_unique,
        ]

    def validate_username_unique(self) -> None:
        if not self.repository.is_username_free(self.create_data.username):
            raise conflict('username')

    def validate_email(self) -> None:
        if self.normalize_email:
            validate_email(self.normalize_email)

    def validate_email_unique(self) -> None:
        if not self.normalize_email:
            return
        if not self.repository.is_email_free(self.normalize_email):
            raise conflict('email')
