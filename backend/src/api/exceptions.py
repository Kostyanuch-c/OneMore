from dataclasses import dataclass, field
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class ApiRequestError(ApplicationError):
    message: str = 'Request validation error'


@dataclass(eq=False)
class InvalidTimeFilterError(ApiRequestError):
    message: str = 'created_from must be less than created_to'
    extra: dict[str, Any] = field(
        default_factory=lambda: {
            'field': 'created_from',
            'related_field': 'created_to',
        }
    )
    status_code: int = 400


@dataclass(eq=False)
class EmailMustBeStringError(ApiRequestError):
    message: str = 'Email must be a string'
    extra: dict[str, Any] = field(default_factory=lambda: {'field': 'email'})
