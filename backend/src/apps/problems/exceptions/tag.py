from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class TagNotFoundError(ApplicationError):
    message: str = 'Tag not found'
    extra: dict[str, Any] = field(default_factory=lambda: {'field': 'tag_id'})
    status_code: int = HTTPStatus.NOT_FOUND
