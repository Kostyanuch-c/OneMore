from http import HTTPStatus

from ninja import Router, Status

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
    '/login/code/',
    response=ApiResponse[AuthOutSchema],
    url_name='request_login_code',
)
def request_login_code_view(
    request: HttpRequest, payload: AuthInputSchema
) -> ApiResponse[AuthOutSchema]:
    AuthService().request_login_code(email=payload.email)
    return ApiResponse.success(
        data=AuthOutSchema(
            message='If this email is registered, a confirmation code has been sent'
        )
    )


@router.post(
    '/login/confirm/',
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


@router.post(
    '/logout/',
    response={HTTPStatus.NO_CONTENT: None},
    url_name='auth_logout',
)
def logout_view(request: HttpRequest) -> Status[None]:
    AuthService().logout(request=request)
    return Status(HTTPStatus.NO_CONTENT, None)
