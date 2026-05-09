from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.problems.schemas import ProblemOutSchema
from api.v1.subjects.schemas import ProblemFiltersOutSchema
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.services.problem import ProblemService
from apps.problems.use_case.problem_filters import GetProblemFilters


router = Router(tags=['problems'])
subject_problems_router = Router(tags=['problems'])


@subject_problems_router.get(
    '/filters/',
    response=ApiResponse[ProblemFiltersOutSchema],
    url_name='subject_problems_filters',
)
def get_problems_filters(
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
def get_problem_detail(
    request: HttpRequest,
    problem_id: int,
) -> ApiResponse[ProblemOutSchema]:
    problem = ProblemService().get_problem_detail(
        problem_id=problem_id, user=request.user
    )

    return ApiResponse.success(data=ProblemOutSchema.from_entity(problem))
