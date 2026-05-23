from ninja import Query, Router
from ninja.security import django_auth_is_staff

from django.http import HttpRequest

from api.filters import PaginationIn, PaginationOut
from api.schemas import ApiResponse, ListPaginationResponse, MessageSchema
from api.v1.admin.filters import UserFiltersIn
from api.v1.profile.schemas import UserInputSchema, UserOutSchema
from api.v1.utils import get_authenticated_user
from apps.a12n.services import AuthEmailService
from apps.access.services import TutorStudentMembershipService
from apps.users.dto import UserFilters
from apps.users.services import UserService
from apps.users.use_cases import InviteUser


router = Router(tags=['admin'], auth=django_auth_is_staff)


@router.post(
    '/user/',
    response=ApiResponse[MessageSchema],
    url_name='admin_user_invite',
)
def invite_user_view(
    request: HttpRequest,
    payload: UserInputSchema,
) -> ApiResponse[MessageSchema]:
    tutor = get_authenticated_user(request)

    InviteUser(
        user_service=UserService(),
        code_service=AuthEmailService(),
        tutor_user_membership_service=TutorStudentMembershipService(),
        student_email=payload.email,
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )()
    return ApiResponse.success(data=MessageSchema(message='Invite sent'))


@router.get(
    '/users/',
    response=ApiResponse[ListPaginationResponse[UserOutSchema]],
    url_name='admin_users_list',
)
def get_users_list_view(
    request: HttpRequest,
    filters: Query[UserFiltersIn],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[UserOutSchema]]:
    users_page = UserService().get_users_page(
        filters=UserFilters(**filters.model_dump()),
        offset=pagination_in.offset,
        limit=pagination_in.limit,
    )

    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=users_page.total,
    )

    items = [UserOutSchema.from_entity(obj) for obj in users_page.items]

    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )
