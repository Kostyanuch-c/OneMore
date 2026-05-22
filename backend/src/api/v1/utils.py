from typing import TYPE_CHECKING, cast

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


if TYPE_CHECKING:
    from apps.users.models import User


def get_authenticated_user(request: HttpRequest) -> User:
    return cast('User', request.user)


def get_tutor_user(request: HttpRequest) -> User:
    user = get_authenticated_user(request)

    if user.is_staff or user.is_tutor:
        return user

    raise PermissionDenied
