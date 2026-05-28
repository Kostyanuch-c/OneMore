from typing import Any

from pydantic.fields import Field

from ninja import Schema

from api.filters import PaginationOut


class ApiError(Schema, extra='forbid'):
    message: str
    extra: dict[str, Any] | None = Field(default_factory=dict)


class ListResponse[TListSchema](Schema, extra='forbid'):
    items: list[TListSchema]


class ListPaginationResponse[TListSchema](Schema, extra='forbid'):
    items: list[TListSchema]
    pagination: PaginationOut


class MessageSchema(Schema, extra='forbid'):
    message: str


class ApiResponse[TData](Schema, extra='forbid'):
    data: TData | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[ApiError] = Field(default_factory=list)

    @classmethod
    def success(
        cls,
        data: TData,
        meta: dict[str, Any] | None = None,
    ) -> ApiResponse[TData]:
        return cls(data=data, meta=meta or {})

    @classmethod
    def failure(
        cls,
        message: str | None = None,
        extra: dict[str, Any] | None = None,
        errors: list[ApiError] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> ApiResponse[TData]:
        if errors:
            return cls(errors=errors, meta=meta or {})

        return cls(
            errors=[
                ApiError(
                    message=message or 'Unknown error',
                    extra=extra or {},
                ),
            ],
            meta=meta or {},
        )
