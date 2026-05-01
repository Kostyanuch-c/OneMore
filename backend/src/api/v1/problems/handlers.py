from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.problems.schemas import ProblemFiltersOutSchema
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.use_case.problem_filters import GetProblemFilters


router = Router(tags=['problems'])


@router.get(
    '/subjects/{subject_slug}/problem-filters/',
    response=ApiResponse[ProblemFiltersOutSchema],
    url_name='problems_filters',
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
