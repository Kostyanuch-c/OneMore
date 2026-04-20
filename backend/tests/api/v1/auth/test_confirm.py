import json
from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf, lfc

from tests.api.utils import (
    assert_api_failure_response,
    assert_api_success_response,
    assert_errors_structure,
    get_api_data,
    get_api_errors,
)

from api.v1.auth.schemas import AuthUserOutSchema


def test_auth_confirm_code_success(
    auth_confirm_url: str,
    client,
    student,
    authorise_and_get_code,
) -> None:
    code = authorise_and_get_code(student.email)

    payload = json.dumps({'code': code, 'email': student.email})
    response = client.post(
        auth_confirm_url,
        data=payload,
        content_type='application/json',
    )

    assert_api_success_response(response=response)
    data = get_api_data(response=response, schema=AuthUserOutSchema)
    assert data.user.email == student.email


@pytest.mark.parametrize(
    'payload',
    [
        {'code': 'invalid_code', 'email': lf('student.email')},
        {
            'code': lfc(
                lambda authorise_and_get_code, student: authorise_and_get_code(
                    student.email
                )
            ),
            'email': 'email_not_exist@mail.ru',
        },
    ],
)
def test_auth_confirm_invalid_code_or_email_not_exist(
    auth_confirm_url: str,
    client,
    payload,
) -> None:
    response = client.post(
        auth_confirm_url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    assert_api_failure_response(response, HTTPStatus.BAD_REQUEST)
    errors = get_api_errors(response)
    assert_errors_structure(errors)
    assert len(errors) == 1
    assert errors[0].message == 'Invalid or expired code'


def test_auth_confirm_invalid_email(
    auth_confirm_url: str,
    client,
) -> None:
    response = client.post(
        auth_confirm_url,
        data=json.dumps({'code': 'invalid_code', 'email': 'invalid_email'}),
        content_type='application/json',
    )
    assert_api_failure_response(response, HTTPStatus.UNPROCESSABLE_CONTENT)
