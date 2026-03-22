from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass
class AccessContextError(ApplicationError):
    message = 'Access context error'


@dataclass
class TutorStudentIntegrityError(AccessContextError):
    message = 'Unique together tutor-student constraint violation'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': ['tutor_id', 'student_id']}
    )
    status_code: int = HTTPStatus.CONFLICT


@dataclass
class TutorSelfInviteError(AccessContextError):
    message = 'Tutor cannot invite himself'
    extra: dict[str, Any] = field(
        default_factory=lambda: {
            'field': 'email',
            'reason': 'self_invite',
        }
    )
    status_code: int = HTTPStatus.CONFLICT
