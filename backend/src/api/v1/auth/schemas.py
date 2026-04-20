from ninja import Schema

from api.v1.profile.schemas import EmailSchema, UserOutSchema
from apps.users.entities import UserEntity


class AuthInputSchema(EmailSchema, extra='forbid'): ...


class AuthOutSchema(Schema, extra='forbid'):
    message: str


class ConfirmEmailInputSchema(EmailSchema, extra='forbid'):
    code: str


class InviteTokenConfirmIn(Schema, extra='forbid'):
    token: str


class AuthUserOutSchema(Schema, extra='forbid'):
    user: UserOutSchema

    @classmethod
    def from_entity(cls, user: UserEntity) -> AuthUserOutSchema:
        return cls(user=UserOutSchema.from_entity(user))
