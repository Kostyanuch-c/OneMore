import json
from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

from tests.api.utils import (
    assert_api_failure_response,
    assert_api_success_response,
    assert_api_unauthorized_response,
    assert_user_state_in_db,
    get_api_data,
    get_api_errors,
)

from api.v1.profile.schemas import UserOutSchema


UPDATE_PAYLOAD = {
    'username': 'New_username',
    'first_name': 'New_name',
    'last_name': 'New_last_name',
}


def test_get_profile_me_success(
    tutor_client,
    profile_me_get_url: str,
    tutor,
) -> None:
    response = tutor_client.get(profile_me_get_url)

    assert_api_success_response(response=response)
    user_data = get_api_data(response=response, schema=UserOutSchema)

    assert user_data.email == tutor.email
    assert user_data.username == tutor.username
    assert user_data.id == tutor.id
    assert user_data.is_staff == tutor.is_staff


def test_get_profile_me_unauthorized(
    client,
    profile_me_get_url: str,
) -> None:
    response = client.get(profile_me_get_url)
    assert_api_unauthorized_response(response=response)


@pytest.mark.parametrize(
    ('_client', 'payload', 'status'),
    [
        (lf('client'), UPDATE_PAYLOAD, HTTPStatus.UNAUTHORIZED),
        (
            lf('random_auth_client'),
            {**UPDATE_PAYLOAD, 'admin': True},
            HTTPStatus.UNPROCESSABLE_CONTENT,
        ),
    ],
    ids=[
        'unauthorized',
        'unprocessable_content_extra_admin_field',
    ],
)
def test_patch_profile_me_invalid_cases(
    _client,
    profile_me_update_url: str,
    status: HTTPStatus,
    payload,
    django_user_model,
    random_user,
) -> None:
    response = _client.patch(
        profile_me_update_url,
        data=json.dumps(payload),
        content_type='application/json',
    )

    if status == HTTPStatus.UNAUTHORIZED:
        assert_api_unauthorized_response(response=response)
    else:
        assert response.status_code == status
        assert set(response.json().keys()) == {'detail'}

        detail = response.json()['detail']
        assert isinstance(detail, list)
        assert all(
            {'loc', 'msg', 'type'} <= set(item.keys()) for item in detail
        )

        assert_user_state_in_db(
            user_from_db=django_user_model.objects.get(id=random_user.id),
            source_user=random_user,
        )


@pytest.mark.parametrize(
    'payload',
    [UPDATE_PAYLOAD, {'username': 'new_username'}],
    ids=['full_allowed_update', 'username_only_update'],
)
def test_patch_profile_me_success(
    student_client,
    student,
    profile_me_update_url: str,
    payload,
    django_user_model,
) -> None:
    response = student_client.patch(
        profile_me_update_url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    assert_api_success_response(response=response)
    new_user_data = get_api_data(response=response, schema=UserOutSchema)

    assert new_user_data.username == payload['username']
    assert new_user_data.first_name == payload.get(
        'first_name', student.first_name
    )
    assert new_user_data.last_name == payload.get(
        'last_name', student.last_name
    )
    assert new_user_data.id == student.id
    assert new_user_data.email == student.email
    assert new_user_data.is_staff == student.is_staff

    student_from_db = django_user_model.objects.get(id=student.id)
    assert_user_state_in_db(
        user_from_db=student_from_db, source_user=student, payload=payload
    )
    assert django_user_model.objects.count() == 1


def test_patch_profile_me_update_username_already_exists(
    student_client,
    student,
    profile_me_update_url: str,
    user_factory,
    django_user_model,
) -> None:
    username = 'existing_username'
    user_factory.create(username=username)
    response = student_client.patch(
        profile_me_update_url,
        data=json.dumps({'username': username}),
        content_type='application/json',
    )
    assert_api_failure_response(response, HTTPStatus.CONFLICT)

    errors = get_api_errors(response)
    assert len(errors) == 1
    extra = errors[0].extra
    assert isinstance(extra, dict)
    assert extra['field'] == 'username'

    assert_user_state_in_db(
        user_from_db=django_user_model.objects.get(id=student.id),
        source_user=student,
    )
    assert django_user_model.objects.count() == 1 + 1
