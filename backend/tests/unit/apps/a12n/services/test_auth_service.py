import pytest

from apps.a12n.exceptions.email import (
    InvalidInviteTokenError,
    InvalidLoginCodeError,
)
from apps.users.entities import UserEntity


@pytest.mark.parametrize('user', [None, object()])
def test_auth_service_authorise(auth_service, mocker, email, user):
    get_user_mock = mocker.patch.object(
        auth_service,
        '_find_user_by_email',
        return_value=user,
    )
    send_code_mock = mocker.patch.object(
        auth_service.code_service,
        'send_login_code',
        return_value=None,
    )

    result = auth_service.request_login_code(email=email)

    assert result is None
    get_user_mock.assert_called_once_with(email=email)

    if user is not None:
        send_code_mock.assert_called_once_with(email=email)
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
    user_entity_and_user,
):
    user_entity, user = (
        user_entity_and_user
        if user_exists
        else (user_entity_and_user[0], None)
    )
    request = object()
    code = 'some_code'

    get_user_mock = mocker.patch.object(
        auth_service,
        '_find_user_by_email',
        return_value=user,
    )
    verify_code_mock = mocker.patch.object(
        auth_service.code_service,
        'verify_login_code',
        return_value=is_verify,
    )
    login_mock = mocker.patch.object(
        auth_service.auth_strategy,
        'login',
        return_value=None,
    )

    if should_raise:
        with pytest.raises(InvalidLoginCodeError):
            auth_service.confirm(request=request, email=email, code=code)
    else:
        result = auth_service.confirm(
            request=request,
            email=email,
            code=code,
        )

        assert isinstance(result, UserEntity)
        assert result == user_entity

    get_user_mock.assert_called_once_with(email=email)

    if user is None:
        verify_code_mock.assert_not_called()
        login_mock.assert_not_called()
    elif not is_verify:
        verify_code_mock.assert_called_once_with(email=email, code=code)
        login_mock.assert_not_called()
    else:
        verify_code_mock.assert_called_once_with(email=email, code=code)
        login_mock.assert_called_once_with(request=request, user=user)


def test_auth_service_invite_confirm_success(
    auth_service,
    user_factory,
    mocker,
    code_service_mock,
    email,
    login_session_mock,
    user_entity_and_user,
    get_user_model_by_email_mock,
):
    user_entity, user = user_entity_and_user
    request = object()
    token = '123445'  # noqa
    get_user_model_by_email_mock.return_value = user

    code_service_mock.verify_invite_token.return_value = email
    auth_service.code_service = code_service_mock

    result = auth_service.invite_confirm(request=request, token=token)
    assert isinstance(result, UserEntity)
    assert result == user_entity

    login_session_mock.assert_called_once_with(request=request, user=user)
    code_service_mock.verify_invite_token.assert_called_once_with(token=token)
    get_user_model_by_email_mock.assert_called_once_with(email=email)


def test_auth_service_invite_confirm_user_not_found(
    auth_service,
    mocker,
    code_service_mock,
    login_session_mock,
):
    request = object()
    token = '123445'  # noqa
    email = 'test@example.com'

    get_user_mock = mocker.patch.object(
        auth_service,
        '_find_user_by_email',
        return_value=None,
    )

    code_service_mock.verify_invite_token.return_value = email
    auth_service.code_service = code_service_mock

    with pytest.raises(RuntimeError):
        auth_service.invite_confirm(request=request, token=token)

    code_service_mock.verify_invite_token.assert_called_once_with(token=token)
    get_user_mock.assert_called_once_with(email=email)
    login_session_mock.assert_not_called()


def test_auth_service_invite_confirm_invalid_token(
    auth_service,
    mocker,
    code_service_mock,
    login_session_mock,
    get_user_model_by_email_mock,
):
    request = object()
    token = '123445'  # noqa

    code_service_mock.verify_invite_token.return_value = None
    auth_service.code_service = code_service_mock

    with pytest.raises(InvalidInviteTokenError):
        auth_service.invite_confirm(request=request, token=token)

    code_service_mock.verify_invite_token.assert_called_once_with(token=token)
    get_user_model_by_email_mock.assert_not_called()
    login_session_mock.assert_not_called()
