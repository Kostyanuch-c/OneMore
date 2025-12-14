import os
from .base import *

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")
allowed_hosts_env = os.getenv("ALLOWED_HOSTS")
ALLOWED_HOSTS = allowed_hosts_env.split(",") if allowed_hosts_env else []
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ALLOW_ALL_ORIGINS = False
cors_origins_env = os.getenv("CORS_ORIGIN_WHITELIST")
CORS_ORIGIN_WHITELIST = cors_origins_env.split(",") if cors_origins_env else []
