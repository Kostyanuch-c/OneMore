from ninja import Router

from django.http import HttpRequest


router = Router(tags=['posts'])


@router.get('/hello')
def hello(request: HttpRequest) -> dict[str, str]:
    return {'message': 'Hello World'}
