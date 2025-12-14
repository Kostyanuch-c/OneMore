from django.http import HttpRequest

from ninja import Router


router = Router(tags=['posts'])


@router.get('/hello')
def hello(request: HttpRequest) -> dict[str, str]:
    return {"message": "Hello World"}
