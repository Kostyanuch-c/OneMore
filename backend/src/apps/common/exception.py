from dataclasses import dataclass, field
from typing import Any

from api.schemas import ApiError


@dataclass(eq=False)
class ApplicationError(Exception):
    message: str = 'Application error'
    meta: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)
    errors: list[ApiError] = field(default_factory=list)
    status_code: int = 422

    def __post_init__(self) -> None:
        """Needed for use error.args and str(error)"""
        super().__init__(self.message)

    def as_list(self) -> list[ApiError]:
        """Return list of ApiError objects for ApiResponse"""
        if self.errors:
            return self.errors
        return [
            ApiError(
                message=self.message,
                extra=self.extra,
            ),
        ]
