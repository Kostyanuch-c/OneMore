from typing import Any

from api.schemas import ApiError


class ApplicationError(Exception):
    def __init__(
        self,
        message: str | None = None,
        meta: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        errors: list[ApiError] | None = None,
        status_code: int = 422,
    ) -> None:
        """
        message/extra одиночная ошибка
        errors список ошибок
        """
        super().__init__(message)
        self.message = message
        self.meta = meta or {}
        self.extra = extra or {}
        self.errors = errors or []
        self.status_code = status_code

    def as_list(self) -> list[ApiError]:
        """Возвращает список ошибок для ApiResponse"""
        if self.errors:
            return self.errors
        return [
            ApiError(
                message=self.message or "Unknown error",
                extra=self.extra,
            ),
        ]
