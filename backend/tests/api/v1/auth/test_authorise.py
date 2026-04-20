import json
from http import HTTPStatus

from tests.api.utils import (
    assert_api_failure_response,
    assert_api_success_response,
    get_api_data,
)

from api.v1.auth.schemas import AuthOutSchema


def test_auth_authorise_success(
    auth_authorise_url: str, client, student, mailoutbox, extract_login_code
) -> None:
    payload = json.dumps({'email': student.email})
    response = client.post(
        auth_authorise_url, data=payload, content_type='application/json'
    )

    assert_api_success_response(response=response)

    data = get_api_data(response=response, schema=AuthOutSchema)
    assert len(data.message) > 1
    assert len(mailoutbox) == 1

    code_message = mailoutbox[0]
    code = extract_login_code(code_message.body)

    assert code is not None
    assert code_message.to == [student.email]


def test_auth_authorise_nonexistent_email_returns_success_without_sending_email(
    mailoutbox, auth_authorise_url: str, client
) -> None:
    payload = json.dumps({'email': 'not_exist_email@mail.ru'})
    response = client.post(
        auth_authorise_url, data=payload, content_type='application/json'
    )

    assert_api_success_response(response=response)
    data = get_api_data(response=response, schema=AuthOutSchema)
    assert len(data.message) > 1
    assert len(mailoutbox) == 0


def test_auth_authorise_invalid_email(
    mailoutbox, auth_authorise_url: str, client
) -> None:
    payload = json.dumps({'email': 'invalid_email'})
    response = client.post(
        auth_authorise_url, data=payload, content_type='application/json'
    )
    assert_api_failure_response(response, HTTPStatus.UNPROCESSABLE_CONTENT)
    assert len(mailoutbox) == 0
