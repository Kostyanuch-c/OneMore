from django.db import IntegrityError

from apps.common.base_exeption import ApplicationError


def conflict(field: str, message: str | None = None) -> ApplicationError:
    return ApplicationError(
        message=message or f'{field} already exists',
        extra={'field': field},
        status_code=409,
    )


def constraint_name(e: IntegrityError) -> str | None:
    cause = getattr(e, '__cause__', None)
    diag = getattr(cause, 'diag', None)
    return getattr(diag, 'constraint_name', None)


def normalize_email_strict(email: str | None) -> str | None:
    return email.strip().lower() if email else None
