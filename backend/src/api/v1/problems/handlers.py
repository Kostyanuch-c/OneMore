from http import HTTPStatus

from ninja import Router, Status
from ninja.security import django_auth_is_staff

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.problems.schemas import (
    ProblemCreateInSchema,
    ProblemMutationOutSchema,
    ProblemOutSchema,
)
from api.v1.subjects.schemas import ProblemFiltersOutSchema
from api.v1.utils import get_authenticated_user
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.services import TagService, TopicService
from apps.problems.services.problem import ProblemService
from apps.problems.use_case.create_problem import CreateProblemUseCase
from apps.problems.use_case.problem_filters import GetProblemFilters


router = Router(tags=['problems'])
subject_problems_router = Router(tags=['problems'])


@subject_problems_router.get(
    '/filters/',
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


@subject_problems_router.post(
    '/',
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

    created_problem = CreateProblemUseCase(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        tag_service=TagService(),
        subject_slug=subject_slug,
        create_data=payload.to_dto(author_id=user.id),
    )()

    return Status(
        HTTPStatus.CREATED,
        ApiResponse.success(
            data=ProblemMutationOutSchema.from_result(result=created_problem)
        ),
    )
