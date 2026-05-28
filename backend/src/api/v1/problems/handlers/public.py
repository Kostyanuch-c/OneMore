from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse, ListResponse
from api.v1.problems.schemas import ProblemListItemOutSchema, ProblemOutSchema
from apps.problems.services import ProblemService


router = Router(tags=['Public Problems'])


@router.get(
    '/recent/',
    response=ApiResponse[ListResponse[ProblemListItemOutSchema]],
    url_name='recents_problems_list',
)
def get_recent_problems_list_view(
    request: HttpRequest,
) -> ApiResponse[ListResponse[ProblemListItemOutSchema]]:
    problems = ProblemService().get_recent_problems()
    items = [
        ProblemListItemOutSchema.from_entity(entity=problem)
        for problem in problems
    ]
    return ApiResponse.success(data=ListResponse(items=items))


@router.get(
    '/{problem_id}/',
    response=ApiResponse[ProblemOutSchema],
    url_name='problem_detail',
    exclude_none=True,
)
def get_public_problem_detail_view(
    request: HttpRequest,
    problem_id: int,
) -> ApiResponse[ProblemOutSchema]:
    problem = ProblemService().get_public_problem_detail(
        problem_id=problem_id,
        user=request.user,
    )

    return ApiResponse.success(
        data=ProblemOutSchema.from_entity(entity=problem, user=request.user)
    )
