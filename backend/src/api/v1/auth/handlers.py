from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.auth.schemas import (
    AuthInputSchema,
    AuthOutSchema,
    ConfirmEmailInputSchema,
    ConfirmEmailOutSchema,
)
from api.v1.profile.schemas import UserOutSchema
from apps.a12n.services import AuthService


router = Router(tags=['auth'])


@router.post(
    '/authorise',
    response=ApiResponse[AuthOutSchema],
)
def authorise_view(
    request: HttpRequest, payload: AuthInputSchema
) -> ApiResponse[AuthOutSchema]:
    AuthService().authorise(payload.email)
    return ApiResponse.success(data=AuthOutSchema(ok=True))


@router.post(
    '/confirm',
    response=ApiResponse[ConfirmEmailOutSchema],
)
def confirm_view(
    request: HttpRequest, payload: ConfirmEmailInputSchema
) -> ApiResponse[ConfirmEmailOutSchema]:
    user = AuthService().confirm(
        email=payload.email, code=payload.code, request=request
    )
    if user is None:
        raise ValueError('Invalid code')
    user_data = UserOutSchema.from_entity(user)
    return ApiResponse.success(data=ConfirmEmailOutSchema(user=user_data))
