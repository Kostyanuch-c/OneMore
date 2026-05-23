from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.problems.schemas import ProblemOutSchema
from apps.problems.services import ProblemService


router = Router(tags=['Public Problems'])


@router.get(
    '/{problem_id}/',
    response=ApiResponse[ProblemOutSchema],
    url_name='problem_detail',
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
