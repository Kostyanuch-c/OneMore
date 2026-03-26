from django.core.cache import cache

import pytest

from apps.a12n.services.code import AuthEmailService


@pytest.fixture
def code_service():
    return AuthEmailService()


def test_verify_login_code_integration(code_service):
    email = 'test@example.com'
    code = '123456'

    # Set cache
    cache.set(code_service._login_code_key(email), code)

    # Verify
    assert code_service.verify_login_code(email, code) is True
    # Verify it's deleted after success
    assert cache.get(code_service._login_code_key(email)) is None


def test_verify_login_code_max_attempts(code_service, settings):
    settings.EMAIL_CODE_MAX_VERIFY_ATTEMPTS = 2
    email = 'test@example.com'
    code = '123456'

    cache.set(code_service._login_code_key(email), code)

    # Attempt 1
    assert code_service.verify_login_code(email, 'wrong') is False
    # Attempt 2 - should delete code
    assert code_service.verify_login_code(email, 'wrong') is False

    assert cache.get(code_service._login_code_key(email)) is None
