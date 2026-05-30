from http import HTTPStatus

from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError

from django.core.exceptions import (
    PermissionDenied,
    ValidationError as DjangoValidationError,
)
from django.db import IntegrityError
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
)
from django.urls import path

from api.schemas import (
    ApiError,
    ApiResponse,
)
from api.v1.urls import router as v1_router
from apps.common.exception import ApplicationError


api = NinjaAPI(version='1.0.0', urls_namespace='api-v1')

api.add_router('v1/', v1_router)

urlpatterns = [
    path('', api.urls),
]


@api.exception_handler(NinjaValidationError)
def ninja_validation_error_handler(
    request: HttpRequest,
    exc: NinjaValidationError,
) -> HttpResponse:
    errors: list[ApiError] = []

    for error in exc.errors:
        loc = error.get('loc', [])
        field = loc[-1] if loc else None

        errors.append(
            ApiError(
                message=error.get('msg', 'Invalid input'),
                extra={
                    'field': field,
                    'loc': loc,
                    'type': error.get('type'),
                    'ctx': error.get('ctx'),
                },
            )
        )

    return api.create_response(
        request,
        ApiResponse.failure(errors=errors),
        status=HTTPStatus.UNPROCESSABLE_CONTENT,
    )


@api.exception_handler(Http404)
def http404_exception_handler(
    request: HttpRequest,
    exc: Http404,
) -> HttpResponse:
    return api.create_response(
        request,
        ApiResponse.failure(message='Not found', extra={}),
        status=HTTPStatus.NOT_FOUND,
    )


@api.exception_handler(Exception)
def exception_handler(
    request: HttpRequest,
    exc: Exception,
) -> HttpResponse:
    # Custom errors
    if isinstance(exc, ApplicationError):
        return api.create_response(
            request,
            ApiResponse.failure(errors=exc.as_list(), meta=exc.meta),
            status=exc.status_code,
        )

    # Django validation errors
    if isinstance(exc, DjangoValidationError):
        errors: list[ApiError] = []

        error_dict = getattr(exc, 'error_dict', None)
        if error_dict:
            for field, err_list in error_dict.items():
                errors.append(
                    ApiError(
                        message=', '.join(str(e) for e in err_list),
                        extra={'field': field},
                    )
                )
        else:
            errors.append(ApiError(message=', '.join(map(str, exc.messages))))

        return api.create_response(
            request,
            ApiResponse.failure(errors=errors),
            status=HTTPStatus.UNPROCESSABLE_CONTENT,
        )

    # Permission errors
    if isinstance(exc, PermissionDenied):
        return api.create_response(
            request,
            ApiResponse.failure(message='Permission denied', extra={}),
            status=HTTPStatus.FORBIDDEN,
        )

    # DB constraint / unique errors
    if isinstance(exc, IntegrityError):
        return api.create_response(
            request,
            ApiResponse.failure(message='Integrity error', extra={}),
            status=HTTPStatus.CONFLICT,
        )

    # Other errors
    return api.create_response(
        request,
        ApiResponse.failure(
            message='Internal server error',
            extra={},
        ),
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
