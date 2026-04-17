from datetime import datetime
from typing import Any

from pydantic import field_validator

from ninja import Schema

from django.core.validators import validate_email

from api.exceptions import EmailMustBeStringError
from apps.common.utils import normalize_email_strict
from apps.users.entities import UserEntity
from apps.users.models import User
from apps.users.repositories.converter import UserConverter


class EmailSchema(Schema):
    email: str

    @field_validator('email', mode='before')
    @classmethod
    def normalize_email(cls, email: Any) -> str | None:
        if email is None:
            return None
        if not isinstance(email, str):
            raise EmailMustBeStringError

        normalized_email = normalize_email_strict(email)
        validate_email(normalized_email)
        return normalized_email


class UserOutSchema(Schema, extra='forbid'):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    email: str
    username: str
    is_active: bool
    is_staff: bool
    date_joined: datetime

    @staticmethod
    def from_entity(entity: UserEntity) -> UserOutSchema:
        return UserOutSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.full_name,
            email=entity.email,
            username=entity.username,
            is_active=entity.is_active,
            is_staff=entity.is_staff,
            date_joined=entity.date_joined,
        )

    @staticmethod
    def from_model(model: User) -> UserOutSchema:
        return UserOutSchema.from_entity(UserConverter.to_entity(model))


class UserInputSchema(EmailSchema, extra='forbid'):
    email: str


class UserUpdateSchema(Schema, extra='forbid'):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
