from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass(eq=False)
class TopicNotFoundError(ApplicationError):
    message: str = 'Problem not found'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': 'topic_id'}
    )
    status_code: int = HTTPStatus.NOT_FOUND
