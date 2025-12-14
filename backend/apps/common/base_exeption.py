from typing import Any


class ApplicationError(Exception):
    def __init__(
        self,
        message: str,
        meta: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        status_code: int = 422,
    ) -> None:
        self.message = message
        self.meta = meta or {}
        self.extra = extra or {}
        self.status_code = status_code
