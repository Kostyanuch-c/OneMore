from http import HTTPStatus

from ninja import Query, Router, Status
from ninja.security import django_auth_is_staff

from django.http import HttpRequest

from api.filters import PaginationIn, PaginationOut
from api.schemas import ApiResponse, ListPaginationResponse
from api.v1.problems.filters import ProblemsFilterInSchema
from api.v1.problems.schemas import (
    ProblemCreateInSchema,
    ProblemMutationOutSchema,
    ProblemOutSchema,
    ProblemUpdateInSchema,
)
from api.v1.subjects.schemas import ProblemFiltersOutSchema
from api.v1.utils import get_authenticated_user
from apps.problems.dto import ProblemFilters
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.services import ProblemService, TagService, TopicService
from apps.problems.use_case import (
    CreateProblemUseCase,
    GetProblemFilters,
    UpdateProblemUseCase,
)


router = Router(tags=['problems'])
subject_problems_router = Router(tags=['problems'])


@router.get(
    '/{problem_id}/',
    response=ApiResponse[ProblemOutSchema],
    url_name='problem_detail',
)
def get_problem_detail_view(
    request: HttpRequest,
    problem_id: int,
) -> ApiResponse[ProblemOutSchema]:
    problem = ProblemService().get_problem_detail(
        problem_id=problem_id, user=request.user
    )

    return ApiResponse.success(data=ProblemOutSchema.from_entity(problem))


@router.delete(
    '/{problem_id}/',
    response={HTTPStatus.NO_CONTENT: None},
    url_name='problems_delete',
    auth=django_auth_is_staff,
)
def delete_problem_view(
    request: HttpRequest,
    problem_id: int,
) -> Status[None]:
    ProblemService().delete_problem(problem_id=problem_id)

    return Status(HTTPStatus.NO_CONTENT, None)


@subject_problems_router.get(
    '{subject_slug}/problems/list/',
    response=ApiResponse[ListPaginationResponse[ProblemOutSchema]],
    url_name='subject_problems_list',
)
def get_problems_list_view(
    request: HttpRequest,
    subject_slug: str,
    filters: Query[ProblemsFilterInSchema],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[ProblemOutSchema]]:
    problems_page = ProblemService().get_problems_page(
        filters=ProblemFilters(
            subject_slug=subject_slug, **filters.model_dump()
        ),
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        user=request.user,
    )

    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=problems_page.total,
    )
    items = [
        ProblemOutSchema.from_entity(problem)
        for problem in problems_page.items
    ]
    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out)
    )


@subject_problems_router.get(
    '{subject_slug}/problems/filters/',
    response=ApiResponse[ProblemFiltersOutSchema],
    url_name='subject_problems_filters',
)
def get_problems_filters_view(
    request: HttpRequest,
    subject_slug: str,
) -> ApiResponse[ProblemFiltersOutSchema]:
    problems_filters = GetProblemFilters(
        subject_repository=SubjectRepository(),
        section_repository=SectionRepository(),
        topic_repository=TopicRepository(),
        tag_repository=TagRepository(),
        subject_slug=subject_slug,
    )()

    return ApiResponse(
        data=ProblemFiltersOutSchema.from_result(problems_filters)
    )


@subject_problems_router.post(
    '{subject_slug}/problems/',
    response={
        HTTPStatus.CREATED: ApiResponse[ProblemMutationOutSchema],
    },
    url_name='subject_problems_create',
    auth=django_auth_is_staff,
)
def create_problem_view(
    request: HttpRequest,
    payload: ProblemCreateInSchema,
    subject_slug: str,
) -> Status[ApiResponse[ProblemMutationOutSchema]]:
    user = get_authenticated_user(request)

    redirect_data = CreateProblemUseCase(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        tag_service=TagService(),
        subject_slug=subject_slug,
        create_data=payload.to_dto(author_id=user.id),
    )()

    return Status(
        HTTPStatus.CREATED,
        ApiResponse.success(
            data=ProblemMutationOutSchema.from_result(result=redirect_data)
        ),
    )


@subject_problems_router.patch(
    '{subject_slug}/problems/{problem_id}/',
    response=ApiResponse[ProblemMutationOutSchema],
    url_name='subject_problems_update',
    auth=django_auth_is_staff,
)
def update_problem_view(
    request: HttpRequest,
    payload: ProblemUpdateInSchema,
    subject_slug: str,
    problem_id: int,
) -> ApiResponse[ProblemMutationOutSchema]:
    redirect_data = UpdateProblemUseCase(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        tag_service=TagService(),
        subject_slug=subject_slug,
        problem_id=problem_id,
        update_data=payload.to_dto(),
    )()

    return ApiResponse.success(
        data=ProblemMutationOutSchema.from_result(result=redirect_data)
    )
