from datetime import (
    datetime,
    timezone as dt_timezone,
)

from django.db import IntegrityError

import pytest

from apps.users.dto import UserFilters, UserUpdateDTO
from apps.users.exceptions.users import (
    EmailAlreadyExistsError,
    UserCreateConflictError,
    UserNameAlreadyExistsError,
)


DATE_FROM = datetime(2024, 1, 1, tzinfo=dt_timezone.utc)
DATE_TO = datetime(2024, 12, 31, tzinfo=dt_timezone.utc)


def test_get_users_page_builds_query_and_calls_repository(
    mocker,
    user_repository_mock,
    user_service,
):
    filters = UserFilters(is_active=True)
    built_query = object()
    expected_users = [object(), object()]
    expected_total = 10
    limit = 10
    offset = 5

    build_query_mock = mocker.patch.object(
        user_service,
        '_build_user_list_query',
        return_value=built_query,
    )

    user_repository_mock.get_users_list.return_value = expected_users
    user_repository_mock.get_users_count.return_value = expected_total
    user_service.repository = user_repository_mock

    result = user_service.get_users_page(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    build_query_mock.assert_called_once_with(filters=filters)

    user_repository_mock.get_users_list.assert_called_once_with(
        filters=built_query,
        limit=limit,
        offset=offset,
    )
    user_repository_mock.get_users_count.assert_called_once_with(
        filters=built_query,
    )

    assert result.items == expected_users
    assert result.total == expected_total


def test_get_user_by_email_calls_repository(
    user_repository_mock, user_service
):
    expected_user = object()
    email = 'example@mail.ru'
    include_inactive = False

    user_repository_mock.get_user_by_email.return_value = expected_user
    user_service.repository = user_repository_mock

    result = user_service.get_user_by_email(
        email=email,
        include_inactive=include_inactive,
    )

    user_repository_mock.get_user_by_email.assert_called_once_with(
        email=email,
        include_inactive=include_inactive,
    )
    assert result is expected_user


@pytest.mark.parametrize(
    ('conflict_field', 'expected_exception'),
    [
        ('email', EmailAlreadyExistsError),
        ('username', UserNameAlreadyExistsError),
        (None, UserCreateConflictError),
    ],
)
def test_create_user_raises_custom_error_on_integrity_error(
    mocker,
    user_service,
    user_repository_mock,
    conflict_field,
    expected_exception,
):
    user_repository_mock.create_user.side_effect = IntegrityError('some error')
    user_service.repository = user_repository_mock
    mocker.patch.object(
        user_service,
        '_detect_user_conflict_field',
        return_value=conflict_field,
    )

    with pytest.raises(expected_exception):
        user_service.create_user(email='test@test.ru', username='test')


def test_create_user_calls_repository_with_correct_data(
    user_repository_mock,
    user_service,
):
    payload = {'email': 'test@test.ru', 'username': 'test'}
    expected_user = object()

    user_repository_mock.create_user.return_value = expected_user
    user_service.repository = user_repository_mock

    result = user_service.create_user(**payload)

    user_repository_mock.create_user.assert_called_once_with(**payload)
    assert result is expected_user


@pytest.mark.parametrize(
    ('field', 'expected_exception'),
    [
        ('username', UserNameAlreadyExistsError),
        ('unknown_field', IntegrityError),
    ],
)
def test_update_user_maps_integrity_error_based_on_user_data(
    mocker, user_service, field, expected_exception
):
    username = 'new_username' if field == 'username' else None
    user_data = UserUpdateDTO(username=username)

    mocker.patch.object(
        user_service.repository,
        'update_user',
        side_effect=IntegrityError('some unknown integrity error'),
    )

    with pytest.raises(expected_exception):
        user_service.update_user(user_id=1, user_data=user_data)


def test_update_user_calls_repository_and_returns_result(
    user_repository_mock, user_service
):
    expected_user = object()
    user_id = 1
    user_data = {'username': 'new_username'}

    user_repository_mock.update_user.return_value = expected_user
    user_service.repository = user_repository_mock
    result = user_service.update_user(user_id=user_id, user_data=user_data)

    user_repository_mock.update_user.assert_called_once_with(
        user_id=user_id, user_data=user_data
    )
    assert result is expected_user


@pytest.mark.parametrize(
    ('constraint_name', 'expected_field'),
    [
        ('users_user_email_key', 'email'),
        ('users_user_username_key', 'username'),
        ('some_other_key', None),
        ('USERS_USER_EMAIL_KEY', 'email'),
        ('USERS_USER_USERNAME_KEY', 'username'),
    ],
)
def test_detect_user_conflict_field_by_diag(
    mocker,
    user_service,
    constraint_name,
    expected_field,
):
    diag_mock = mocker.Mock()
    diag_mock.constraint_name = constraint_name

    cause_mock = Exception()
    cause_mock.diag = diag_mock

    exc = IntegrityError('some message')
    exc.__cause__ = cause_mock

    assert user_service._detect_user_conflict_field(exc=exc) == expected_field


@pytest.mark.parametrize(
    ('message', 'expected_field'),
    [
        (
            'duplicate key value violates unique constraint "users_user_email_key"',
            'email',
        ),
        (
            'duplicate key value violates unique constraint "users_user_username_key"',
            'username',
        ),
        ('EMAIL already exists', 'email'),
        ('USERNAME already exists', 'username'),
        ('some other error', None),
    ],
)
def test_detect_user_conflict_field_by_message(
    user_service,
    message,
    expected_field,
):
    exc = IntegrityError(message)

    assert user_service._detect_user_conflict_field(exc=exc) == expected_field


def test_detect_user_conflict_field_falls_back_to_message_when_diag_not_matched(
    mocker,
    user_service,
):
    diag_mock = mocker.Mock()
    diag_mock.constraint_name = 'some_other_key'

    cause_mock = Exception()
    cause_mock.diag = diag_mock

    exc = IntegrityError(
        'duplicate key value violates unique constraint "users_user_email_key"'
    )
    exc.__cause__ = cause_mock

    assert user_service._detect_user_conflict_field(exc=exc) == 'email'
