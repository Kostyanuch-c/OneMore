from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class SolutionNotFoundError(ApplicationError):
    message: str = 'Solution not found'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'solution_id'}
    )
    status_code: int = HTTPStatus.NOT_FOUND


@dataclass(eq=False)
class MainSolutionCannotBeHiddenError(ApplicationError):
    message: str = 'Main solution cannot be hidden'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'is_published'}
    )
    status_code: int = HTTPStatus.CONFLICT
