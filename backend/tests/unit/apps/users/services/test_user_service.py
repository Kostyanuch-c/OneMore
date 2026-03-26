from datetime import (
    datetime,
    timezone as dt_timezone,
)

from django.db import IntegrityError
from django.db.models import Q

import pytest

from tests.integration.utils.user_helpers import assert_q_equal

from apps.users.exceptions.users import (
    EmailAlreadyExistsError,
    UserCreateConflictError,
    UserNameAlreadyExistsError,
)
from apps.users.filters import UserFilters


DATE_FROM = datetime(2024, 1, 1, tzinfo=dt_timezone.utc)
DATE_TO = datetime(2024, 12, 31, tzinfo=dt_timezone.utc)


def test_get_users_count_calls_build_query_and_repository(
    mocker, user_service
):
    filters = UserFilters(is_active=True)
    built_query = object()
    mock_result = 10
    build_query_mock = mocker.patch.object(
        user_service,
        '_build_user_query',
        return_value=built_query,
    )
    repository_mock = mocker.patch.object(
        user_service.repository,
        'get_users_count',
        return_value=mock_result,
    )

    result = user_service.get_users_count(filters)

    build_query_mock.assert_called_once_with(filters)
    repository_mock.assert_called_once_with(filters=built_query)
    assert result == mock_result


def test_get_users_list_calls_build_query_and_repository(mocker, user_service):
    filters = UserFilters(is_active=True)
    built_query = object()
    expected_users = [object(), object()]
    limit = 10
    offset = 5

    build_query_mock = mocker.patch.object(
        user_service,
        '_build_user_query',
        return_value=built_query,
    )
    repository_mock = mocker.patch.object(
        user_service.repository,
        'get_users_list',
        return_value=expected_users,
    )

    result = user_service.get_users_list(
        filters=filters, limit=limit, offset=offset
    )

    build_query_mock.assert_called_once_with(filters)
    repository_mock.assert_called_once_with(
        filters=built_query, limit=limit, offset=offset
    )
    assert result == expected_users


def test_get_user_by_email_calls_repository(mocker, user_service):
    expected_user = object()
    email = 'example@mail.ru'
    include_inactive = False

    mock_repository = mocker.patch.object(
        user_service.repository,
        'get_user_by_email',
        return_value=expected_user,
    )

    result = user_service.get_user_by_email(
        email=email,
        include_inactive=include_inactive,
    )

    mock_repository.assert_called_once_with(
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
    conflict_field,
    expected_exception,
):
    mocker.patch.object(
        user_service.repository,
        'create_user',
        side_effect=IntegrityError('some unknown integrity error'),
    )
    mocker.patch.object(
        user_service,
        '_detect_user_conflict_field',
        return_value=conflict_field,
    )

    with pytest.raises(expected_exception):
        user_service.create_user(email='test@test.ru', username='test')


def test_create_user_calls_repository_with_correct_data(
    mocker,
    user_service,
):
    payload = {'email': 'test@test.ru', 'username': 'test'}
    expected_user = object()

    mock_repository = mocker.patch.object(
        user_service.repository, 'create_user', return_value=expected_user
    )

    result = user_service.create_user(**payload)

    mock_repository.assert_called_once_with(**payload)
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
    user_data = {field: 'new_value'}

    mocker.patch.object(
        user_service.repository,
        'update_user',
        side_effect=IntegrityError('some unknown integrity error'),
    )

    with pytest.raises(expected_exception):
        user_service.update_user(user_id=1, user_data=user_data)


def test_update_user_calls_repository_and_returns_result(mocker, user_service):
    expected_user = object()
    user_id = 1
    user_data = {'username': 'new_username'}

    mock_repository = mocker.patch.object(
        user_service.repository,
        'update_user',
        return_value=expected_user,
    )
    result = user_service.update_user(user_id=user_id, user_data=user_data)

    mock_repository.assert_called_once_with(
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

    assert user_service._detect_user_conflict_field(exc) == expected_field


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

    assert user_service._detect_user_conflict_field(exc) == expected_field


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

    assert user_service._detect_user_conflict_field(exc) == 'email'


@pytest.mark.parametrize(
    ('filters', 'expected_query'),
    [
        (UserFilters(), Q()),
        (UserFilters(is_active=False), Q(is_active=False)),
        (
            UserFilters(search='john'),
            (
                Q(username__icontains='john')
                | Q(email__icontains='john')
                | Q(first_name__icontains='john')
                | Q(last_name__icontains='john')
            ),
        ),
        (UserFilters(created_from=DATE_FROM), Q(date_joined__gte=DATE_FROM)),
        (UserFilters(created_to=DATE_TO), Q(date_joined__lte=DATE_TO)),
        (
            UserFilters(
                is_active=True,
                search='john',
                created_from=DATE_FROM,
                created_to=DATE_TO,
            ),
            Q(is_active=True)
            & (
                Q(username__icontains='john')
                | Q(email__icontains='john')
                | Q(first_name__icontains='john')
                | Q(last_name__icontains='john')
            )
            & Q(date_joined__gte=DATE_FROM)
            & Q(date_joined__lte=DATE_TO),
        ),
    ],
)
def test_build_user_query_returns_query_with_filters(
    user_service,
    filters,
    expected_query,
):
    result = user_service._build_user_query(filters)

    assert_q_equal(result, expected_query)
