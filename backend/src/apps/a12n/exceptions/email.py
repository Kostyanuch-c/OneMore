from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass
class EmailAuthError(ApplicationError):
    message = 'Email authentication error'


@dataclass
class InvalidLoginCodeError(EmailAuthError):
    message: str = 'Invalid or expired code'
    extra: dict[str, Any] = field(default_factory=dict)
    status_code: int = HTTPStatus.BAD_REQUEST
