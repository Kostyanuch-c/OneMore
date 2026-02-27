from datetime import datetime
from typing import Any

from pydantic import field_validator

from ninja import Schema

from django.core.validators import validate_email

from api.exceptions import EmailMustBeStringError
from apps.common.utils import normalize_email_strict
from apps.users.entities import UserEntity


class EmailSchema(Schema):
    email: str | None = None

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


class UserOutSchema(Schema):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    email: str | None = None
    username: str
    role: str
    created_at: datetime

    @staticmethod
    def from_entity(entity: UserEntity) -> UserOutSchema:
        return UserOutSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.full_name,
            email=entity.email,
            username=entity.username,
            created_at=entity.created_at,
            role=entity.role,
        )


class UserInputSchema(EmailSchema):
    password: str
    username: str

    class Config:
        extra = 'forbid'


class UserUpdateSchema(EmailSchema):
    # Потом здесь вместо user_id будет token и будет расшифровывать и проверять
    user_id: int
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        extra = 'forbid'
