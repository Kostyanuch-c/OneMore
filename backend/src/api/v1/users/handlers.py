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
from api.v1.users.filters import UserFiltersIn
from api.v1.users.schemas import (
    UserInputSchema,
    UserOutSchema,
)
from apps.users.filters import UserFilters
from apps.users.repositories.user_repository import UserRepository
from apps.users.services import UserCreator, UsersListCount


router = Router(tags=['users'])


@router.post(
    '/',
    response=ApiResponse[UserOutSchema],
)
def create_user_view(
    request: HttpRequest,
    payload: UserInputSchema,
) -> ApiResponse[UserOutSchema]:
    user = UserCreator(payload)()
    return ApiResponse.success(data=UserOutSchema.from_entity(user))


@router.get(
    '/',
    response=ApiResponse[ListPaginationResponse[UserOutSchema]],
)
def get_user_list(
    request: HttpRequest,
    filters: Query[UserFiltersIn],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[UserOutSchema]]:
    users_page = UsersListCount(
        repo=UserRepository(),
        filters=UserFilters(**filters.dict()),
        offset=pagination_in.offset,
        limit=pagination_in.limit,
    )()
    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=users_page.total,
    )

    items = [UserOutSchema.from_entity(obj) for obj in users_page.items]

    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )
