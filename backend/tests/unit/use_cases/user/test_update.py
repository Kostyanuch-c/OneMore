import pytest

from apps.users.dto import UserUpdateDTO
from apps.users.exceptions.users import UserNameAlreadyExistsError
from apps.users.use_cases import UpdateUser


@pytest.mark.usefixtures('transaction_mock')
def test_use_case_update_user_calls_service(user_service_mock, user_entity):
    user_data = UserUpdateDTO(username='new_username')
    expected = user_entity

    user_service_mock.update_user.return_value = expected

    result = UpdateUser(
        service=user_service_mock,
        user_id=1,
        user_data=user_data,
    )()

    user_service_mock.update_user.assert_called_once_with(
        user_id=1,
        user_data=user_data,
    )
    assert result == expected


@pytest.mark.usefixtures('transaction_mock')
def test_use_case_update_user_propagates_error(user_service_mock):
    user_data = UserUpdateDTO(username='new_username')
    user_id = 1

    user_service_mock.update_user.side_effect = UserNameAlreadyExistsError
    with pytest.raises(UserNameAlreadyExistsError):
        UpdateUser(
            service=user_service_mock,
            user_id=user_id,
            user_data=user_data,
        )()

    user_service_mock.update_user.assert_called_once_with(
        user_id=user_id,
        user_data=user_data,
    )
