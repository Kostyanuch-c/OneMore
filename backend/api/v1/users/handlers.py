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
from api.v1.users.schemas import (
    UserInputSchema,
    UserOutSchema,
)
from apps.users.services.user_service import UserCreator, UserService


router = Router(tags=['users'])


@router.post(
    '/',
    response=ApiResponse[UserOutSchema],
)
def create_user_view(
    _request: HttpRequest,
    payload: UserInputSchema,
) -> ApiResponse[UserOutSchema]:
    user = UserCreator(payload)()
    return ApiResponse.success(data=UserOutSchema.from_entity(user))


@router.get(
    '/',
    response=ApiResponse[ListPaginationResponse[UserOutSchema]],
)
def get_user_list(
    _request: HttpRequest,
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
