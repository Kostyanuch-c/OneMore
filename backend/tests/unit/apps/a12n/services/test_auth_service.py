from dataclasses import asdict

import pytest

from apps.a12n.exceptions.email import InvalidLoginCodeError
from apps.users.entities import UserEntity


@pytest.mark.parametrize('user', [None, object()])
def test_auth_service_authorise(auth_service, mocker, email, user):
    get_user_mock = mocker.patch.object(
        auth_service,
        '_get_user_model_by_email',
        return_value=user,
    )
    send_code_mock = mocker.patch.object(
        auth_service.code_service,
        'send_login_code',
        return_value=None,
    )

    result = auth_service.authorise(email)

    assert result is None
    get_user_mock.assert_called_once_with(email)

    if user is not None:
        send_code_mock.assert_called_once_with(email)
    else:
        send_code_mock.assert_not_called()


@pytest.mark.parametrize(
    ('user_exists', 'is_verify', 'should_raise'),
    [
        (False, True, True),
        (False, False, True),
        (True, True, False),
        (True, False, True),
    ],
)
def test_auth_service_confirm(
    auth_service,
    mocker,
    email,
    user_exists,
    is_verify,
    should_raise,
    user_entity,
    user_factory,
):
    build_user_params = asdict(user_entity)
    build_user_params.pop('full_name', None)

    user = user_factory.build(**build_user_params) if user_exists else None
    request = object()
    code = 'some_code'

    get_user_mock = mocker.patch.object(
        auth_service,
        '_get_user_model_by_email',
        return_value=user,
    )
    verify_code_mock = mocker.patch.object(
        auth_service.code_service,
        'verify_login_code',
        return_value=is_verify,
    )
    login_mock = mocker.patch.object(
        auth_service.login_strategy,
        'login',
        return_value=None,
    )

    if should_raise:
        with pytest.raises(InvalidLoginCodeError):
            auth_service.confirm(request, email, code)
    else:
        result = auth_service.confirm(request, email, code)

        assert isinstance(result, UserEntity)
        assert result == user_entity

    get_user_mock.assert_called_once_with(email)

    if user is None:
        verify_code_mock.assert_not_called()
        login_mock.assert_not_called()
    elif not is_verify:
        verify_code_mock.assert_called_once_with(email, code)
        login_mock.assert_not_called()
    else:
        verify_code_mock.assert_called_once_with(email, code)
        login_mock.assert_called_once_with(request, user)
