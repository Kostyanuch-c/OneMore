from http import HTTPStatus

from ninja import Query, Router, Status
from ninja.security import django_auth

from django.http import HttpRequest

from api.filters import PaginationIn, PaginationOut
from api.schemas import ApiResponse, ListPaginationResponse
from api.v1.problems.filters import MyProblemsFilterInSchema
from api.v1.problems.schemas import (
    ProblemCreateInSchema,
    ProblemMutationOutSchema,
    ProblemOutSchema,
    ProblemUpdateInSchema,
)
from api.v1.utils import get_tutor_user
from apps.problems.dto import ProblemFilters
from apps.problems.services import ProblemService, TagService, TopicService
from apps.problems.use_case import CreateProblemUseCase, UpdateProblemUseCase


router = Router(tags=['Tutor Problems'], auth=django_auth)


@router.get(
    '/problems/',
    response=ApiResponse[ListPaginationResponse[ProblemOutSchema]],
    url_name='profile_problems_list',
)
def get_my_problems_list_view(
    request: HttpRequest,
    filters: Query[MyProblemsFilterInSchema],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginationResponse[ProblemOutSchema]]:
    tutor = get_tutor_user(request)

    problems_page = ProblemService().get_my_problems_page(
        filters=ProblemFilters(**filters.model_dump()),
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        user=tutor,
    )

    pagination_out = PaginationOut(
        limit=pagination_in.limit,
        offset=pagination_in.offset,
        total=problems_page.total,
    )

    items = [
        ProblemOutSchema.from_entity(entity=problem, user=tutor)
        for problem in problems_page.items
    ]

    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out)
    )


@router.get(
    '/problems/{problem_id}/',
    response=ApiResponse[ProblemOutSchema],
    url_name='profile_problem_detail',
)
def get_my_problem_detail_view(
    request: HttpRequest,
    problem_id: int,
) -> ApiResponse[ProblemOutSchema]:
    tutor = get_tutor_user(request)

    problem = ProblemService().get_my_problem_detail(
        problem_id=problem_id,
        user=tutor,
    )

    return ApiResponse.success(
        data=ProblemOutSchema.from_entity(entity=problem, user=tutor)
    )


@router.patch(
    '/subjects/{subject_slug}/problems/{problem_id}/',
    response=ApiResponse[ProblemMutationOutSchema],
    url_name='profile_problem_update',
)
def update_my_problem_view(
    request: HttpRequest,
    payload: ProblemUpdateInSchema,
    subject_slug: str,
    problem_id: int,
) -> ApiResponse[ProblemMutationOutSchema]:
    tutor = get_tutor_user(request)

    redirect_data = UpdateProblemUseCase(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        tag_service=TagService(),
        subject_slug=subject_slug,
        problem_id=problem_id,
        update_data=payload.to_dto(),
        tutor=tutor,
    )()

    return ApiResponse.success(
        data=ProblemMutationOutSchema.from_result(result=redirect_data)
    )


@router.post(
    '/subjects/{subject_slug}/problems/',
    response={
        HTTPStatus.CREATED: ApiResponse[ProblemMutationOutSchema],
    },
    url_name='profile_problems_create',
)
def create_problem_view(
    request: HttpRequest,
    payload: ProblemCreateInSchema,
    subject_slug: str,
) -> Status[ApiResponse[ProblemMutationOutSchema]]:
    user = get_tutor_user(request)

    redirect_data = CreateProblemUseCase(
        problem_service=ProblemService(),
        topic_service=TopicService(),
        tag_service=TagService(),
        subject_slug=subject_slug,
        create_data=payload.to_dto(author_id=user.pk),
    )()

    return Status(
        HTTPStatus.CREATED,
        ApiResponse.success(
            data=ProblemMutationOutSchema.from_result(result=redirect_data)
        ),
    )


@router.delete(
    '/problems/{problem_id}/',
    response={HTTPStatus.NO_CONTENT: None},
    url_name='profile_problem_delete',
)
def delete_my_problem_view(
    request: HttpRequest,
    problem_id: int,
) -> Status[None]:
    user = get_tutor_user(request)

    ProblemService().delete_my_problem(
        problem_id=problem_id,
        user=user,
    )

    return Status(HTTPStatus.NO_CONTENT, None)
