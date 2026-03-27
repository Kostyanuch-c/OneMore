from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any

from apps.common.exception import ApplicationError


@dataclass
class AccessContextError(ApplicationError):
    message: str = 'Access context error'


@dataclass(eq=False)
class TutorStudentIntegrityError(AccessContextError):
    message: str = 'Invalid tutor-student membership data'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': ['tutor_id', 'student_id']}
    )
    status_code: int = HTTPStatus.CONFLICT


@dataclass(eq=False)
class TutorStudentAlreadyExistsError(AccessContextError):
    message: str = 'Tutor-student membership already exists'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': ['tutor_id', 'student_id']}
    )
    status_code: int = HTTPStatus.CONFLICT


@dataclass(eq=False)
class TutorAndStudentMustBeDifferentError(AccessContextError):
    message: str = 'Tutor and student must be different users'
    extra: dict[str, Any] = field(
        default_factory=lambda: {'field': ['tutor_id', 'student_id']}
    )
    status_code: int = HTTPStatus.CONFLICT


@dataclass
class TutorSelfInviteError(AccessContextError):
    message: str = 'Tutor cannot invite himself'
    extra: dict[str, Any] = field(
        default_factory=lambda: {
            'field': 'email',
            'reason': 'self_invite',
        }
    )
    status_code: int = HTTPStatus.CONFLICT
