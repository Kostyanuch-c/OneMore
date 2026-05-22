import time

from django.conf import settings
from django.core.cache import cache
from django.test import override_settings


def test_auth_email_service_send_login_code(
    mailoutbox,
    auth_email_service,
    email,
):
    auth_email_service.send_login_code(email=email)

    assert len(mailoutbox) == 1

    send_code_message = mailoutbox[0]
    assert send_code_message.subject == f'{settings.SITE_NAME}: код для входа'
    assert send_code_message.from_email == settings.DEFAULT_FROM_EMAIL
    assert send_code_message.to == [email]
    assert (
        f'{settings.EMAIL_CODE_TTL_SECONDS // 60} минут'
        in send_code_message.body
    )

    code = cache.get(auth_email_service._login_code_key(email=email))
    assert code is not None
    assert code in send_code_message.body

    cooldown = cache.get(
        auth_email_service._login_code_cooldown_key(email=email)
    )
    assert cooldown == '1'

    assert len(send_code_message.alternatives) == 1
    html_body, mimetype = send_code_message.alternatives[0]
    assert mimetype == 'text/html'
    assert code in html_body
    assert settings.SITE_NAME in html_body
    assert settings.SITE_URL in html_body
    assert settings.SUPPORT_EMAIL in html_body


@override_settings(EMAIL_CODE_RESEND_COOLDOWN_SECONDS=1)
def test_auth_email_service_send_login_code_respects_cooldown_expiration(
    mailoutbox,
    auth_email_service,
    email,
):
    auth_email_service.send_login_code(email=email)
    assert len(mailoutbox) == 1

    first_code = cache.get(auth_email_service._login_code_key(email=email))
    assert first_code is not None

    auth_email_service.send_login_code(email=email)
    assert len(mailoutbox) == 1

    time.sleep(1.1)

    auth_email_service.send_login_code(email=email)
    assert len(mailoutbox) == 2  # noqa: PLR2004

    second_code = cache.get(auth_email_service._login_code_key(email=email))
    assert second_code is not None
    assert second_code != first_code


def test_auth_email_service_send_login_code_stores_six_digit_code(
    auth_email_service,
    email,
):
    auth_email_service.send_login_code(email=email)

    code = cache.get(auth_email_service._login_code_key(email=email))
    code_length = 6
    assert code is not None
    assert len(code) == code_length
    assert code.isdigit()


def test_auth_email_service_send_invite_link(
    mailoutbox,
    auth_email_service,
    email,
    monkeypatch,
):
    token = 'test-invite-token'  # noqa: S105
    monkeypatch.setattr(auth_email_service, '_generate_token', lambda: token)

    auth_email_service.send_invite_link(email=email)

    assert len(mailoutbox) == 1

    message = mailoutbox[0]
    expected_link = (
        f'{settings.SITE_URL}'
        f'{settings.INVITE_CONFIRM_PATH.rstrip("/")}/{token}/'
    )

    assert message.subject == f'Добро пожаловать в {settings.SITE_NAME}!'
    assert message.from_email == settings.DEFAULT_FROM_EMAIL
    assert message.to == [email]
    assert expected_link in message.body

    payload = cache.get(auth_email_service._invite_token_key(token=token))
    assert payload == {'email': email}

    cooldown = cache.get(
        auth_email_service._invite_email_cooldown_key(email=email)
    )
    assert cooldown == '1'

    assert len(message.alternatives) == 1
    html_body, mimetype = message.alternatives[0]
    assert mimetype == 'text/html'
    assert expected_link in html_body
    assert settings.SITE_NAME in html_body
    assert settings.SITE_URL in html_body
    assert settings.SUPPORT_EMAIL in html_body


@override_settings(INVITE_RESEND_COOLDOWN_SECONDS=1)
def test_auth_email_service_send_invite_link_respects_cooldown_expiration(
    mailoutbox,
    auth_email_service,
    email,
    monkeypatch,
):
    first_token = 'first-token'  # noqa: S105
    second_token = 'second-token'  # noqa: S105
    tokens = iter([first_token, second_token])
    monkeypatch.setattr(
        auth_email_service, '_generate_token', lambda: next(tokens)
    )

    auth_email_service.send_invite_link(email=email)
    assert len(mailoutbox) == 1

    assert cache.get(
        auth_email_service._invite_token_key(token=first_token)
    ) == {'email': email}

    auth_email_service.send_invite_link(email=email)
    assert len(mailoutbox) == 1

    time.sleep(1.1)

    auth_email_service.send_invite_link(email=email)
    assert len(mailoutbox) == 2  # noqa: PLR2004

    assert cache.get(
        auth_email_service._invite_token_key(token=second_token)
    ) == {'email': email}


def test_auth_email_service_verify_login_code_returns_true_for_valid_code(
    auth_email_service,
    email,
):
    auth_email_service.send_login_code(email=email)

    code_key = auth_email_service._login_code_key(email=email)
    attempts_key = auth_email_service._login_code_attempts_key(email=email)
    code = cache.get(code_key)

    assert code is not None

    assert auth_email_service.verify_login_code(email=email, code=code) is True

    assert cache.get(code_key) is None
    assert cache.get(attempts_key) is None


def test_auth_email_service_verify_login_code_returns_false_when_code_missing(
    auth_email_service,
    email,
):
    assert (
        auth_email_service.verify_login_code(email=email, code='123456')
        is False
    )
    assert cache.get(auth_email_service._login_code_key(email=email)) is None
    assert (
        cache.get(auth_email_service._login_code_attempts_key(email=email))
        is None
    )


def test_auth_email_service_verify_login_code_increments_attempts_and_clears_code_on_limit(
    auth_email_service,
    email,
):
    auth_email_service.send_login_code(email=email)

    code_key = auth_email_service._login_code_key(email=email)
    attempts_key = auth_email_service._login_code_attempts_key(email=email)
    code = cache.get(code_key)

    assert code is not None

    for i in range(settings.EMAIL_CODE_MAX_VERIFY_ATTEMPTS - 1):
        assert (
            auth_email_service.verify_login_code(email=email, code='123456')
            is False
        )
        assert cache.get(attempts_key) == i + 1
        assert cache.get(code_key) == code

    assert (
        cache.get(attempts_key) == settings.EMAIL_CODE_MAX_VERIFY_ATTEMPTS - 1
    )

    assert (
        auth_email_service.verify_login_code(email=email, code='123456')
        is False
    )

    assert cache.get(code_key) is None
    assert cache.get(attempts_key) is None

    assert (
        auth_email_service.verify_login_code(email=email, code=code) is False
    )


def test_auth_email_service_verify_invite_token_returns_email_and_deletes_token(
    auth_email_service,
    email,
    monkeypatch,
):
    token = 'test-invite-token'  # noqa: S105
    monkeypatch.setattr(auth_email_service, '_generate_token', lambda: token)

    auth_email_service.send_invite_link(email=email)

    assert auth_email_service.verify_invite_token(token=token) == email
    assert cache.get(auth_email_service._invite_token_key(token=token)) is None


def test_auth_email_service_verify_invite_token_returns_none_when_token_missing(
    auth_email_service,
):
    missing_token = 'missing-token'  # noqa: S105
    assert auth_email_service.verify_invite_token(token=missing_token) is None
