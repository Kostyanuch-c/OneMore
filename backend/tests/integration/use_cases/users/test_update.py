import pytest

from apps.users.dto import UserUpdateDTO
from apps.users.entities import UserEntity
from apps.users.use_cases import UpdateUser


def test_use_case_update_user_happy_path(user_factory, user_service):
    user = user_factory.create()
    new_data = {
        'username': 'new_username',
        'first_name': 'New_name',
        'last_name': 'New_last_name',
    }

    result = UpdateUser(
        service=user_service,
        user_id=user.id,
        user_data=UserUpdateDTO(**new_data),
    )()
    assert isinstance(result, UserEntity)
    assert result.username == new_data['username']
    assert result.first_name == new_data['first_name']
    assert result.last_name == new_data['last_name']


def test_use_case_update_user_when_user_id_does_not_exist(
    user_service,
    nonexistent_id,
):
    with pytest.raises(user_service.repository.user_model.DoesNotExist):
        UpdateUser(
            service=user_service,
            user_id=nonexistent_id,
            user_data=UserUpdateDTO(username='new_username'),
        )()
