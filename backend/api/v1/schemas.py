from typing import (
    Any,
    Generic,
    TypeVar,
)

from ninja import Schema

from api.v1.filters import PaginationOut
from pydantic.fields import Field


TData = TypeVar("TData")
TListSchema = TypeVar("TListSchema")


class ApiError(Schema):
    message: str
    extra: dict[str, Any] | None = Field(default_factory=dict)


class ListPaginationResponse(Schema, Generic[TListSchema]):
    items: list[TListSchema]
    pagination: PaginationOut


class ApiResponse(Schema, Generic[TData]):
    data: TData | dict[Any, Any] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[ApiError] = Field(default_factory=list)

    @classmethod
    def success(
        cls,
        data: TData,
        meta: dict[str, Any] | None = None,
    ) -> 'ApiResponse[TData]':
        return cls(data=data, meta=meta or {})

    @classmethod
    def failure(
        cls,
        message: str | None = None,
        extra: dict[str, Any] | None = None,
        errors: list[ApiError] | None = None,
    ) -> 'ApiResponse[TData]':
        if errors:
            return cls(errors=errors)

        return cls(
            errors=[
                ApiError(
                    message=message or "Unknown error",
                    extra=extra or {},
                ),
            ],
        )
