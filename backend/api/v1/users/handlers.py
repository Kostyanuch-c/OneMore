from django.http import HttpRequest

from ninja import (
    Query,
    Router,
)

from api.filters import (
    PaginationIn,
    PaginationOut,
)
from api.schemas import (
    ApiResponse,
    ListPaginationResponse,
)
from api.v1.users.schemas import UserOutSchema
from apps.users.entities import UserInputSchema
from apps.users.services.user_service import UserService


router = Router(tags=['users'])


@router.post(
    "/",
    response=ApiResponse[UserOutSchema],
)
def create_user_view(
    request: HttpRequest,
    payload: UserInputSchema,
) -> ApiResponse[UserOutSchema]:
    user = UserService().create_object(payload)
    return ApiResponse.success(
        data=UserOutSchema(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            username=user.username,
            created_at=user.created_at,
        ),
    )


@router.get(
    "/",
    response=ApiResponse[ListPaginationResponse[UserOutSchema]],
)
def get_user_list(
    request: HttpRequest,
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[UserOutSchema]]:
    service = UserService()
    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=service.get_users_count(),
    )

    items = [
        UserOutSchema.from_entity(obj) for obj in service.get_all_objects()
    ]

    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )
