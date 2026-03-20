from ninja import Schema

from api.v1.profile.schemas import EmailSchema, UserOutSchema


class AuthInputSchema(EmailSchema): ...


class AuthOutSchema(Schema):
    ok: bool


class ConfirmEmailInputSchema(EmailSchema):
    code: str


class ConfirmEmailOutSchema(Schema):
    user: UserOutSchema
