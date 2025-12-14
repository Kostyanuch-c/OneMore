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

from ninja import NinjaAPI

from api.v1.urls import router as v1_router
from apps.common.base_exeption import ApplicationError


api = NinjaAPI()


# @api.get("/ping", response=PingResponseSchema)
# def ping(request: HttpRequest) -> PingResponseSchema:
#     return PingResponseSchema(result=True)


api.add_router('v1/', v1_router)

urlpatterns = [
    path("", api.urls),
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
            {"message": exc.message, "extra": exc.extra},
            status=exc.status_code,
        )

    # Django validation errors
    if isinstance(exc, DjangoValidationError):
        return api.create_response(
            request,
            {
                "message": "Validation error",
                "extra": {"fields": exc.message_dict},
            },
            status=422,
        )

    # 404 errors
    if isinstance(exc, Http404):
        return api.create_response(
            request,
            {"message": "Not found", "extra": {}},
            status=404,
        )

    # Permission errors
    if isinstance(exc, PermissionDenied):
        return api.create_response(
            request,
            {"message": "Permission denied", "extra": {}},
            status=403,
        )

    # DB constraint / unique errors
    if isinstance(exc, IntegrityError):
        return api.create_response(
            request,
            {"message": "Integrity error", "extra": {"details": str(exc)}},
            status=409,
        )

    # Other errors
    return api.create_response(
        request,
        {
            "message": "Internal server error",
            "extra": {
                "error": str(exc.__class__.__name__),
                "details": str(exc),
            },
        },
        status=500,
    )
