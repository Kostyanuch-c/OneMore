from ninja import NinjaAPI

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


api = NinjaAPI()

api.add_router('v1/', v1_router)

urlpatterns = [
    path('', api.urls),
]


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
            status=422,
        )

    # 404 errors
    if isinstance(exc, Http404):
        return api.create_response(
            request,
            ApiResponse.failure(message='Not found', extra={}),
            status=404,
        )

    # Permission errors
    if isinstance(exc, PermissionDenied):
        return api.create_response(
            request,
            ApiResponse.failure(message='Permission denied', extra={}),
            status=403,
        )

    # DB constraint / unique errors
    if isinstance(exc, IntegrityError):
        return api.create_response(
            request,
            ApiResponse.failure(
                message='Integrity error',
                extra={'details': str(exc)},
            ),
            status=409,
        )

    # Other errors
    return api.create_response(
        request,
        ApiResponse.failure(
            message='Internal server error',
            extra={
                'error': str(exc.__class__.__name__),
                'details': str(exc),
            },
        ),
        status=500,
    )
