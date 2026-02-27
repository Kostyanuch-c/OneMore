from django.db import IntegrityError


def constraint_name(e: IntegrityError) -> str | None:
    cause = getattr(e, '__cause__', None)
    diag = getattr(cause, 'diag', None)
    return getattr(diag, 'constraint_name', None)


def normalize_email_strict(email: str) -> str:
    return email.strip().lower()
