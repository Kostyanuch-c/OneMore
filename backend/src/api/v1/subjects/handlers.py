from ninja import Router

from django.http import HttpRequest

from api.schemas import ApiResponse
from api.v1.subjects.schemas import SubjectOutSchema
from apps.problems.repositories import (
    SubjectRepository,
)


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
