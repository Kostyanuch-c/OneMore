from collections.abc import Callable
from urllib.parse import urlencode

from django.urls import reverse

import pytest


@pytest.fixture
def profile_me_get_url() -> str:
    return reverse('api-v1:profile_me_get')


@pytest.fixture
def profile_me_update_url() -> str:
    return reverse('api-v1:profile_me_update')


@pytest.fixture
def auth_authorise_url() -> str:
    return reverse('api-v1:auth_authorise')


@pytest.fixture
def auth_invite_confirm_url() -> Callable[[str], str]:
    def _make_url(token: str) -> str:
        return reverse(
            'api-v1:auth_invite_confirm',
            kwargs={'token': token},
        )

    return _make_url


@pytest.fixture
def auth_confirm_url() -> str:
    return reverse('api-v1:auth_confirm')


@pytest.fixture
def admin_user_invite_url() -> str:
    return reverse('api-v1:admin_user_invite')


@pytest.fixture
def admin_users_list_url() -> Callable[..., str]:
    def _build_url(**query_params) -> str:
        base_url = reverse('api-v1:admin_users_list')
        if query_params:
            return f'{base_url}?{urlencode(query_params)}'
        return base_url

    return _build_url
