from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class SubjectNotFoundError(ApplicationError):
    message: str = 'Subject not found'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'subject_slug'}
    )
    status_code: int = HTTPStatus.NOT_FOUND
