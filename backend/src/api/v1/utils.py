from typing import TYPE_CHECKING, cast

from django.http import HttpRequest


if TYPE_CHECKING:
    from apps.users.models import User


def get_authenticated_user(request: HttpRequest) -> User:
    return cast('User', request.user)
