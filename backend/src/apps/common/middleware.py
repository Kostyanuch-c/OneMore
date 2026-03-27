import logging
import time
import uuid


logger = logging.getLogger('apps.requests')


# TODO - Change logging formatter to json logs,
#  for use in ElasticSearch and check one more time django-structlog package
class ApiRequestLoggingMiddleware:
    def __init__(self, get_response):  # type: ignore
        self.get_response = get_response

    def __call__(self, request):  # type: ignore
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        start = time.perf_counter()

        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request.request_id = request_id

        user_id = None
        if hasattr(request, 'user') and getattr(
            request.user, 'is_authenticated', False
        ):
            user_id = request.user.id

        try:
            response = self.get_response(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                'API request failed | request_id=%s method=%s path=%s user_id=%s duration_ms=%s',
                request_id,
                request.method,
                request.path,
                user_id,
                duration_ms,
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        response['X-Request-ID'] = request_id

        logger.info(
            'API request finished | request_id=%s method=%s path=%s status=%s user_id=%s duration_ms=%s',
            request_id,
            request.method,
            request.path,
            response.status_code,
            user_id,
            duration_ms,
        )
        return response
