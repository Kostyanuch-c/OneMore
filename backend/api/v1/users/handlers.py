from django.http import HttpRequest

from ninja import Router

from api.v1.schemas import ApplicationErrorSchema
from api.v1.users.schemas import UserOutSchema
from apps.users.entities import UserInputSchema
from apps.users.services.user_service import UserService


router = Router(tags=['users'])


@router.post(
    "/",
    response={
        200: UserOutSchema,
        409: ApplicationErrorSchema,
    },
)
def create_user_view(
    request: HttpRequest,
    payload: UserInputSchema,
) -> UserOutSchema:
    user = UserService().create_object(payload)
    return UserOutSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        username=user.username,
        created_at=user.created_at,
    )
