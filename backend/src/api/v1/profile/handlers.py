from ninja import (
    Router,
)
from ninja.security import SessionAuth

from django.http import HttpRequest

from api.schemas import (
    ApiResponse,
)
from api.v1.profile.schemas import UserOutSchema, UserUpdateSchema
from apps.users.services import UserService
from apps.users.use_cases import UpdateUser


router = Router(tags=['profile'], auth=SessionAuth())


@router.post(
    '/me',
    response=ApiResponse[UserOutSchema],
)
def update_user_view(
    request: HttpRequest,
    payload: UserUpdateSchema,
) -> ApiResponse[UserOutSchema]:
    user = UpdateUser(
        service=UserService(),
        user_id=payload.user_id,
        update_data=payload.dict(exclude={'user_id'}, exclude_none=True),
    )()
    return ApiResponse.success(data=UserOutSchema.from_entity(user))
