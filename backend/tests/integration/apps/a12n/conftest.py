from django.core.cache import caches
from django.test.utils import override_settings

import pytest


@pytest.fixture(autouse=True)
def clear_django_cache():
    with override_settings(
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': 'redis://127.0.0.1:6379/2',
            }
        }
    ):
        caches['default'].clear()
        yield
        caches['default'].clear()
