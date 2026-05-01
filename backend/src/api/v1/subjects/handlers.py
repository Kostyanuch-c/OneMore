from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.subjects.schemas import ProblemFiltersOutSchema, SubjectOutSchema
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.use_case.problem_filters import GetProblemFilters


router = Router(tags=['subjects'])


@router.get(
    '/',
    response=ApiResponse[list[SubjectOutSchema]],
    url_name='subjects_list',
)
def get_subjects(request: HttpRequest) -> ApiResponse[list[SubjectOutSchema]]:
    subjects = SubjectRepository().get_list_subjects()

    return ApiResponse(
        data=[SubjectOutSchema.from_entity(subject) for subject in subjects]
    )


@router.get(
    '/{subject_slug}/problem-filters/',
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
