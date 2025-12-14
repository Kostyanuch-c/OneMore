from functools import wraps
from typing import (
    Any,
    Callable,
    ParamSpec,
    TypeVar,
)

from django.db import IntegrityError

from .base_exeption import ApplicationError


P = ParamSpec("P")
R = TypeVar("R")


def handle_unique_field(
    field: str,
    check_exist_func: Callable[..., bool],
    data_index: int,
    id_index: int | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор проверяет уникальность поля если оно присутствует в данных.
    Ловит IntegrityError и преобразует его в ApplicationError.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> R:
            data, object_id = args[data_index], (
                args[id_index] if id_index is not None else None
            )

            value = getattr(data, field, None)
            if value is not None and not check_exist_func(value, object_id):
                raise ApplicationError(
                    message=f"{field.capitalize()} already exists",
                    extra={"field": field},
                    status_code=409,
                )

            try:
                return func(self, *args, **kwargs)
            except IntegrityError as e:
                if field in str(e):
                    raise ApplicationError(
                        message=f"{field.capitalize()} already exists",
                        extra={"field": field},
                        status_code=409,
                    ) from e
                raise

        return wrapper  # type: ignore

    return decorator
