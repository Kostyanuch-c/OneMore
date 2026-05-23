from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class MainSolutionRequiredError(ApplicationError):
    message: str = 'First solution for problem must be main'
    extra: dict[str, Any] = field(default_factory=lambda: {'field': 'is_main'})
    status_code: int = HTTPStatus.CONFLICT


@dataclass(eq=False)
class SolutionNotFoundError(ApplicationError):
    message: str = 'Solution not found'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'solution_id'}
    )
    status_code: int = HTTPStatus.NOT_FOUND
