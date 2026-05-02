from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.problems.schemas import ProblemOutSchema
from apps.problems.repositories.problems import ProblemsRepository


router = Router(tags=['problems'])


@router.get(
    '/{problem_id}/',
    response=ApiResponse[ProblemOutSchema],
    url_name='problem_detail',
)
def get_problem(
    request: HttpRequest,
    problem_id: int,
) -> ApiResponse[ProblemOutSchema]:
    problem = ProblemsRepository().get_problem_by_id(problem_id=problem_id)

    return ApiResponse.success(data=ProblemOutSchema.from_entity(problem))
