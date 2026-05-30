from ninja import Router
from ninja.decorators import decorate_view

from django.http import HttpRequest
from django.views.decorators.cache import cache_page

from api.schemas import ApiResponse
from api.v1.problems.schemas import MainStatisticsOutSchema
from apps.problems.services import (
    ProblemService,
    SectionService,
    SolutionService,
    TopicService,
)
from apps.problems.use_case.get_main_statistic import GetMainStatistic


router = Router(tags=['Main statistics'])


@router.get(
    '/main_statistics/',
    response=ApiResponse[MainStatisticsOutSchema],
    url_name='main_statistics',
    description='Get main statistics of the site.',
)
@decorate_view(cache_page(60 * 15))
def get_main_statistics_view(
    request: HttpRequest,
) -> ApiResponse[MainStatisticsOutSchema]:
    result = GetMainStatistic(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        section_service=SectionService(),
        solution_service=SolutionService(),
    )()

    return ApiResponse.success(
        data=MainStatisticsOutSchema.from_result(result=result)
    )
