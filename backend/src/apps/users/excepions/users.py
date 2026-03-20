from dataclasses import dataclass, field
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class UserServiceError(ApplicationError):
    message: str = 'User service error'


@dataclass(eq=False)
class UserNameAlreadyExistsError(UserServiceError):
    message: str = 'User with this username already exists'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'username'}
    )
    status_code: int = 409


@dataclass(eq=False)
class EmailAlreadyExistsError(UserServiceError):
    message: str = 'User with this email already exists'
    extra: dict[str, Any] = field(default_factory=lambda: {'field': 'email'})
    status_code: int = 409
