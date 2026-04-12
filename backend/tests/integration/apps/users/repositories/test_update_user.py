from django.db import IntegrityError

import pytest

from tests.integration.utils.user_helpers import assert_user_entity_and_model

from apps.users.dto import UserUpdateDTO


@pytest.mark.parametrize(
    'payload_update_user',
    [
        {'username': 'new_username'},
        {'first_name': 'New', 'last_name': 'Name', 'username': 'new_username'},
        {'first_name': 'New', 'last_name': 'Name'},
        {},
    ],
)
def test_update_user_with_different_fields(
    repository,
    user,
    payload_update_user,
    user_model,
):
    user_entity = repository.update_user(
        user_id=user.id,
        user_data=UserUpdateDTO(**payload_update_user),
    )
    db_user_after_update = user_model.objects.get(id=user.id)

    assert user_model.objects.count() == 1

    expected_username = payload_update_user.get('username', user.username)
    expected_first_name = payload_update_user.get(
        'first_name', user.first_name
    )
    expected_last_name = payload_update_user.get('last_name', user.last_name)

    assert_user_entity_and_model(
        user_entity=user_entity,
        db_user=db_user_after_update,
        user_id=user.id,
        email=user.email,
        username=expected_username,
        first_name=expected_first_name,
        last_name=expected_last_name,
    )


def test_update_user_raises_does_not_exist_for_unknown_user(
    repository,
    nonexistent_id,
):
    with pytest.raises(repository.user_model.DoesNotExist):
        repository.update_user(
            user_id=nonexistent_id,
            user_data=UserUpdateDTO(),
        )


def test_update_user_raises_integrity_error_for_username_already_exists(
    repository,
    user,
    user_factory,
):
    username = 'existing_username'
    user_factory.create(username=username)

    with pytest.raises(IntegrityError):
        repository.update_user(
            user_id=user.id,
            user_data=UserUpdateDTO(username=username),
        )
