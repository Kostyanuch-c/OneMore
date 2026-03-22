from http import HTTPStatus

from ninja import Query, Router
from ninja.security import django_auth_is_staff

from django.http import HttpRequest

from api.filters import PaginationIn, PaginationOut
from api.schemas import ApiResponse, ListPaginationResponse
from api.v1.profile.filters import UserFiltersIn
from api.v1.profile.schemas import UserInputSchema, UserOutSchema
from api.v1.utils import get_authenticated_user
from apps.a12n.services import CodeService
from apps.access.services import TutorStudentMembershipService
from apps.users.filters import UserFilters
from apps.users.services import UserService
from apps.users.use_cases import SearchUsers
from apps.users.use_cases.create_user import InviteUser


router = Router(tags=['admin'], auth=django_auth_is_staff)


@router.post(
    '/user',
    response={
        HTTPStatus.CREATED: ApiResponse[UserOutSchema],
        HTTPStatus.OK: ApiResponse[UserOutSchema],
    },
)
def invite_user_view(
    request: HttpRequest,
    payload: UserInputSchema,
) -> tuple[int, ApiResponse[UserOutSchema]]:

    tutor = get_authenticated_user(request)

    user, created = InviteUser(
        user_service=UserService(),
        code_service=CodeService(),
        tutor_user_membership_service=TutorStudentMembershipService(),
        student_email=payload.email,
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )()
    return (
        HTTPStatus.CREATED if created else HTTPStatus.OK,
        ApiResponse.success(data=UserOutSchema.from_entity(user)),
    )


@router.get(
    '/users',
    response=ApiResponse[ListPaginationResponse[UserOutSchema]],
)
def get_user_list(
    request: HttpRequest,
    filters: Query[UserFiltersIn],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[UserOutSchema]]:
    users_page = SearchUsers(
        service=UserService(),
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
