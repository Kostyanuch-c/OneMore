import pytest

from apps.users.dto import UserUpdateDTO
from apps.users.exceptions.users import UserNameAlreadyExistsError
from apps.users.use_cases import UpdateUser


def test_use_case_update_user_calls_service(user_service, mocker, user_entity):
    user_data = UserUpdateDTO(username='new_username')
    expected = user_entity

    update_user_mock = mocker.patch.object(
        user_service,
        'update_user',
        return_value=expected,
    )

    result = UpdateUser(
        service=user_service,
        user_id=1,
        user_data=user_data,
    )()

    update_user_mock.assert_called_once_with(
        user_id=1,
        user_data=user_data,
    )
    assert result == expected


def test_use_case_update_user_propagates_error(user_service, mocker):
    user_data = UserUpdateDTO(username='new_username')

    mocker.patch.object(
        user_service,
        'update_user',
        side_effect=UserNameAlreadyExistsError,
    )

    with pytest.raises(UserNameAlreadyExistsError):
        UpdateUser(
            service=user_service,
            user_id=1,
            user_data=user_data,
        )()
