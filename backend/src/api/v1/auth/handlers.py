from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.auth.schemas import (
    AuthInputSchema,
    AuthOutSchema,
    AuthUserOutSchema,
    ConfirmEmailInputSchema,
    InviteTokenConfirmIn,
)
from apps.a12n.services import AuthService


router = Router(tags=['auth'])


@router.post(
    '/authorise/',
    response=ApiResponse[AuthOutSchema],
    url_name='auth_authorise',
)
def authorise_view(
    request: HttpRequest, payload: AuthInputSchema
) -> ApiResponse[AuthOutSchema]:
    AuthService().authorise(payload.email)
    return ApiResponse.success(
        data=AuthOutSchema(
            message='If this email is registered, a confirmation code has been sent'
        )
    )


@router.post(
    '/confirm/',
    response=ApiResponse[AuthUserOutSchema],
    url_name='auth_confirm',
)
def confirm_view(
    request: HttpRequest, payload: ConfirmEmailInputSchema
) -> ApiResponse[AuthUserOutSchema]:
    user = AuthService().confirm(
        email=payload.email, code=payload.code, request=request
    )
    return ApiResponse.success(data=AuthUserOutSchema.from_entity(user))


@router.post(
    '/invite-confirm/',
    response=ApiResponse[AuthUserOutSchema],
    url_name='auth_invite_confirm',
)
def invite_confirm_view(
    request: HttpRequest,
    payload: InviteTokenConfirmIn,
) -> ApiResponse[AuthUserOutSchema]:
    user = AuthService().invite_confirm(request=request, token=payload.token)
    return ApiResponse.success(data=AuthUserOutSchema.from_entity(user))
