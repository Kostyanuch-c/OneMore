import json
import re
from collections.abc import Callable
from http import HTTPStatus
from urllib.parse import urlencode

from django.urls import reverse

import pytest

from tests.api.utils import assert_api_success_response


@pytest.fixture
def profile_me_get_url() -> str:
    return reverse('api-v1:profile_me_get')


@pytest.fixture
def profile_me_update_url() -> str:
    return reverse('api-v1:profile_me_update')


@pytest.fixture
def auth_authorise_url() -> str:
    return reverse('api-v1:request_login_code')


@pytest.fixture
def auth_invite_confirm_url() -> str:
    return reverse('api-v1:auth_invite_confirm')


@pytest.fixture
def auth_confirm_url() -> str:
    return reverse('api-v1:auth_confirm')


@pytest.fixture
def admin_user_invite_url() -> str:
    return reverse('api-v1:admin_user_invite')


@pytest.fixture
def public_problem_list_url(subject) -> str:
    return reverse(
        'api-v1:subject_problems_list', kwargs={'subject_slug': subject.slug}
    )


@pytest.fixture
def admin_users_list_url() -> Callable[..., str]:
    def _build_url(**query_params) -> str:
        base_url = reverse('api-v1:admin_users_list')
        if query_params:
            return f'{base_url}?{urlencode(query_params)}'
        return base_url

    return _build_url


@pytest.fixture
def extract_login_code() -> Callable[[str], str | None]:
    def _extract_login_code(email_body: str) -> str | None:
        match = re.search(
            r'Введите этот код на сайте, чтобы войти в личный кабинет:\s*(\d{6})',
            email_body,
        )
        return match.group(1) if match else None

    return _extract_login_code


@pytest.fixture
def authorise_and_get_code(
    client,
    auth_authorise_url: str,
    mailoutbox,
    extract_login_code: Callable[[str], str | None],
) -> Callable[[str], str]:
    def _assert_authorise_and_get_code(email: str) -> str:
        payload = json.dumps({'email': email})
        response = client.post(
            auth_authorise_url,
            data=payload,
            content_type='application/json',
        )

        assert_api_success_response(response=response)
        assert len(mailoutbox) == 1

        code = extract_login_code(mailoutbox[0].body)
        assert code is not None
        return code

    return _assert_authorise_and_get_code


@pytest.fixture
def extract_invite_token() -> Callable[[str], str | None]:
    def _extract_invite_token(email_body: str) -> str | None:
        match = re.search(
            r'/auth/invite-confirm/([^/\s]+)/?',
            email_body,
        )
        return match.group(1) if match else None

    return _extract_invite_token


@pytest.fixture
def invite_user_and_get_token(
    tutor_client,
    admin_user_invite_url: str,
    mailoutbox,
    extract_invite_token: Callable[[str], str | None],
    django_capture_on_commit_callbacks,
) -> Callable[[str], str]:
    def _invite_user_and_get_token(email: str) -> str:
        with django_capture_on_commit_callbacks(execute=True) as callbacks:
            response = tutor_client.post(
                admin_user_invite_url,
                data=json.dumps({'email': email}),
                content_type='application/json',
            )
        assert response.status_code == HTTPStatus.OK
        assert len(callbacks) == 1
        assert len(mailoutbox) == 1

        token = extract_invite_token(mailoutbox[0].body)
        assert token is not None
        return token

    return _invite_user_and_get_token
