from typing import TYPE_CHECKING

from ninja import Router


if TYPE_CHECKING:
    from django.http import HttpRequest


router = Router(tags=['posts'])


@router.get('/hello')
def hello(request: HttpRequest) -> dict[str, str]:
    return {'message': 'Hello World'}
