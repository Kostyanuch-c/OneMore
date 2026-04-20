import json
from http import HTTPStatus

from tests.api.utils import (
    assert_api_failure_response,
    assert_api_success_response,
    assert_errors_structure,
    get_api_data,
    get_api_errors,
)

from api.v1.auth.schemas import AuthUserOutSchema


def test_auth_invite_confirm_success(
    auth_invite_confirm_url: str,
    client,
    email_for_create_user: str,
    invite_user_and_get_token,
) -> None:
    token = invite_user_and_get_token(email_for_create_user)

    response = client.post(
        auth_invite_confirm_url,
        data=json.dumps({'token': token}),
        content_type='application/json',
    )
    assert_api_success_response(response=response)
    data = get_api_data(response=response, schema=AuthUserOutSchema)

    assert data.user.email == email_for_create_user


def test_auth_invite_confirm_invalid_token(
    auth_invite_confirm_url: str,
    client,
) -> None:
    token = 'invalid_token_12121'  # noqa: S105

    response = client.post(
        auth_invite_confirm_url,
        data=json.dumps({'token': token}),
        content_type='application/json',
    )
    assert_api_failure_response(response, HTTPStatus.BAD_REQUEST)
    errors = get_api_errors(response)
    assert_errors_structure(errors)

    assert len(errors) == 1
    assert errors[0].message == 'Invalid or expired invite token'
