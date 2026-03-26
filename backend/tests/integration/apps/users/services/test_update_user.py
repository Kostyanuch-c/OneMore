import pytest

from tests.integration.helpers import assert_user_entity_and_model

from apps.users.excepions.users import UserNameAlreadyExistsError


@pytest.mark.parametrize(
    'payload_update',
    [
        {'username': 'new_username'},
        {'first_name': 'New', 'last_name': 'Name', 'username': 'new_username'},
        {'first_name': 'New', 'last_name': 'Name'},
        {},
    ],
)
def test_update_user_with_different_fields(
    user_service, user, payload_update, user_model
):
    user_entity = user_service.update_user(
        user_id=user.id, user_data=payload_update
    )
    db_user_after_update = user_model.objects.get(id=user.id)

    assert user_model.objects.count() == 1

    expected_username = payload_update.get('username', user.username)
    expected_first_name = payload_update.get('first_name', user.first_name)
    expected_last_name = payload_update.get('last_name', user.last_name)

    assert_user_entity_and_model(
        user_entity=user_entity,
        db_user=db_user_after_update,
        user_id=user.id,
        email=user.email,
        username=expected_username,
        first_name=expected_first_name,
        last_name=expected_last_name,
    )


def test_update_user_raise_custom_error_for_username_already_exists(
    user_service, user, user_factory
):
    username = 'existing_username'
    user_factory.create(username=username)

    with pytest.raises(UserNameAlreadyExistsError):
        user_service.update_user(
            user_id=user.id,
            user_data={'username': username},
        )


def test_update_user_raises_value_error_for_not_allowed_fields(
    user_service, user
):
    with pytest.raises(ValueError):  # noqa
        user_service.update_user(
            user_id=user.id,
            user_data={'is_superuser': True},
        )
