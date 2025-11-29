from django.http import HttpRequest

from ninja import Router


router = Router(tags=['posts'])


@router.get('/hello')
def hello(request: HttpRequest) -> dict[str, str]:
    return {"message": "Hello World"}


# Минимальный список объектов
@router.get('')
def items(request: HttpRequest) -> dict[str, list[str]]:
    return {"items": ["apple", "banana", "orange"]}
