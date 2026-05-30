from ninja import Query, Router

from django.http import HttpRequest

from api.filters import PaginationIn, PaginationOut
from api.schemas import ApiResponse, ListPaginationResponse
from api.v1.problems.filters import PublicProblemsFilterInSchema
from api.v1.problems.schemas import ProblemOutSchema
from api.v1.subjects.schemas import ProblemFiltersOutSchema
from apps.problems.dto import PublicProblemFilters
from apps.problems.exceptions import SubjectNotFoundError
from apps.problems.models import Subject
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)
from apps.problems.services import ProblemService
from apps.problems.use_case import GetProblemFilters


router = Router(tags=['Public Problems'])


@router.get(
    '/{subject_slug}/problems/',
    response=ApiResponse[ListPaginationResponse[ProblemOutSchema]],
    url_name='subject_problems_list',
    exclude_none=True,
)
def get_public_problems_list_view(
    request: HttpRequest,
    subject_slug: str,
    filters: Query[PublicProblemsFilterInSchema],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[ProblemOutSchema]]:
    # TODO убрать заглушку на валидацию по предмету, реализовать use_case
    # Заглушка!!!!
    if not Subject.objects.filter(slug=subject_slug).exists():
        raise SubjectNotFoundError

    problems_page = ProblemService().get_public_problems_page(
        filters=PublicProblemFilters(
            subject_slug=subject_slug, **filters.model_dump()
        ),
        offset=pagination_in.offset,
        limit=pagination_in.limit,
    )

    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=problems_page.total,
    )
    items = [
        ProblemOutSchema.from_entity(entity=problem, user=request.user)
        for problem in problems_page.items
    ]
    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out)
    )


@router.get(
    '/{subject_slug}/problems/filters/',
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
