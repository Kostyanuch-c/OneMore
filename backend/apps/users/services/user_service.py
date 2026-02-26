from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404

from api.v1.users.schemas import UserInputSchema, UserUpdateSchema
from apps.common.error_handlers import handle_unique_field
from apps.common.utils import conflict, constraint_name, normalize_email_strict
from apps.users.entities import (
    UserEntity,
)
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository


class BaseService(metaclass=ABCMeta):
    """This is a template of a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments
    """

    def __call__(self) -> Any:
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable]:  # type: ignore[type-arg]
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> Any:
        raise NotImplementedError('Please implement in the service class')


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
        return validate_email(self.normalize_email)

    def validate_email_unique(self) -> None:
        if not self.normalize_email:
            return
        if not self.repository.is_email_free(self.normalize_email):
            raise conflict('email')


class UserService:
    repository = UserRepository()

    def get_users_count(self) -> int:
        return self.repository.get_users_count()

    def get_all_objects(self) -> list[UserEntity]:
        return self.repository.get_all_users()

    def get_user(self, user_id: int) -> UserEntity:
        try:
            return self.repository.get_user_by_id(user_id)
        except User.DoesNotExist:
            raise Http404

    @handle_unique_field(
        field='username',
        check_exist_func=repository.is_username_free,
        data_index=0,
        id_index=0,
    )
    def update_user(
        self,
        user_id: int,
        user_data: UserUpdateSchema,
    ) -> UserEntity:
        return self.repository.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> None:

        return self.repository.delete_object(user_id)
