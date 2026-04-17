import pytest
from pytest_lazy_fixtures import lf

from tests.api.utils import (
    assert_api_paginated_success_response,
    assert_api_unauthorized_response,
    get_api_data,
)

from api.schemas import ListPaginationResponse
from api.v1.profile.schemas import UserOutSchema


def test_get_users_success(
    tutor_client, admin_users_list_url, users, tutor
) -> None:
    filters = {'is_active': True}

    response = tutor_client.get(admin_users_list_url(**filters))
    assert_api_paginated_success_response(response=response)

    data = get_api_data(
        response=response, schema=ListPaginationResponse[UserOutSchema]
    )
    expected_users = sorted(
        [user for user in [*users, tutor] if user.is_active],
        key=lambda u: u.date_joined,
        reverse=True,
    )

    assert [user.id for user in data.items] == [
        user.id for user in expected_users
    ]


def test_get_users_empty(tutor_client, admin_users_list_url) -> None:
    filters = {'is_active': False}
    response = tutor_client.get(admin_users_list_url(**filters))
    assert_api_paginated_success_response(response=response)

    data = get_api_data(
        response=response, schema=ListPaginationResponse[UserOutSchema]
    )

    assert data.items == []
    assert data.pagination.total == 0


@pytest.mark.parametrize('_client', [lf('client'), lf('random_auth_client')])
def test_get_users_unauthorized(_client, admin_users_list_url) -> None:
    response = _client.get(admin_users_list_url())
    assert_api_unauthorized_response(response=response)


# TODO: need to test on auth client status code = 403, right now 401 but its bad.
