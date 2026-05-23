from http import HTTPStatus

from ninja import Router, Status
from ninja.security import django_auth

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.solutions.schemas import (
    SetMainSolutionInSchema,
    SolutionCreateInSchema,
    SolutionMutationOutSchema,
    SolutionUpdateInSchema,
)
from api.v1.utils import get_tutor_user
from apps.problems.services import ProblemService
from apps.problems.services.solution import SolutionService
from apps.problems.use_case import (
    CreateSolutionUseCase,
    SetMainSolutionUseCase,
    UpdateSolutionUseCase,
)


router = Router(tags=['Solutions'], auth=django_auth)


@router.post(
    '/problems/{problem_id}/solutions/',
    response={
        HTTPStatus.CREATED: ApiResponse[SolutionMutationOutSchema],
    },
    url_name='create_solution',
)
def create_solution_view(
    request: HttpRequest,
    payload: SolutionCreateInSchema,
    problem_id: int,
) -> Status[ApiResponse[SolutionMutationOutSchema]]:
    tutor = get_tutor_user(request)

    redirect_data = CreateSolutionUseCase(
        problem_service=ProblemService(),
        solution_service=SolutionService(),
        create_data=payload.to_dto(author_id=tutor.pk, problem_id=problem_id),
    )()

    return Status(
        HTTPStatus.CREATED,
        ApiResponse.success(
            data=SolutionMutationOutSchema.from_result(result=redirect_data)
        ),
    )


@router.patch(
    '/problems/{problem_id}/solutions/{solution_id}/',
    response=ApiResponse[SolutionMutationOutSchema],
    url_name='update_solution',
)
def update_solution_view(
    request: HttpRequest,
    payload: SolutionUpdateInSchema,
    solution_id: int,
    problem_id: int,
) -> ApiResponse[SolutionMutationOutSchema]:
    tutor = get_tutor_user(request)

    redirect_data = UpdateSolutionUseCase(
        problem_service=ProblemService(),
        solution_service=SolutionService(),
        update_data=payload.to_dto(),
        solution_id=solution_id,
        problem_id=problem_id,
        tutor_id=tutor.pk,
    )()

    return ApiResponse.success(
        data=SolutionMutationOutSchema.from_result(result=redirect_data)
    )


@router.patch(
    '/problems/{problem_id}/main-solution/',
    response=ApiResponse[SolutionMutationOutSchema],
    url_name='set_main_solution',
)
def set_main_solution_view(
    request: HttpRequest,
    payload: SetMainSolutionInSchema,
    problem_id: int,
) -> ApiResponse[SolutionMutationOutSchema]:
    tutor = get_tutor_user(request)

    redirect_data = SetMainSolutionUseCase(
        problem_service=ProblemService(),
        solution_service=SolutionService(),
        solution_id=payload.solution_id,
        problem_id=problem_id,
        tutor_id=tutor.pk,
    )()

    return ApiResponse.success(
        data=SolutionMutationOutSchema.from_result(result=redirect_data)
    )
