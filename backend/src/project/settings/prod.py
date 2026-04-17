import os

from .logging import get_logging_config
from .base import *

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY", 'CI_SECRET_KEY')

allowed_hosts_env = os.getenv("ALLOWED_HOSTS")
ALLOWED_HOSTS = allowed_hosts_env.split(",") if allowed_hosts_env else []

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ALLOW_ALL_ORIGINS = False
cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS")
CORS_ALLOWED_ORIGINS = cors_origins_env.split(",") if cors_origins_env else []

SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_SAVE_EVERY_REQUEST = True

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# Todo - Redis
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#     }
# }


EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"
ANYMAIL = {
    "POSTMARK_SERVER_TOKEN": os.getenv('POSTMARK_TOKEN'),
}

LOGGING = get_logging_config(
    base_dir=BASE_DIR,
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_to_file=os.getenv('LOG_TO_FILE', 'true').lower() == "true",
    log_file_name=os.getenv("LOG_FILE_NAME", "app.log"),
    include_test_loggers=False,
)
