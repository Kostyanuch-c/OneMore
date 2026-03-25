import pytest

from tests.integration.helpers import assert_user_entity, assert_user_model


def test_update_user_updates_existing_fields(
    repository,
    user,
    payload_update,
    user_model,
):
    user_entity = repository.update_user(
        user_id=user.id, user_data=payload_update
    )

    assert_user_entity(
        user_entity,
        user_id=user.id,
        email=user.email,
        username=payload_update['username'],
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=payload_update['first_name'],
        last_name=payload_update['last_name'],
    )

    assert user_model.objects.count() == 1

    db_user_after_update = user_model.objects.get(id=user.id)

    assert_user_model(
        db_user_after_update,
        email=user.email,
        username=payload_update['username'],
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=payload_update['first_name'],
        last_name=payload_update['last_name'],
    )


def test_update_user_updates_only_provided_fields(
    repository, user, user_model, payload_update
):
    payload_update.pop('username')

    user_entity = repository.update_user(
        user_id=user.id, user_data=payload_update
    )

    assert_user_entity(
        user_entity,
        user_id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=payload_update['first_name'],
        last_name=payload_update['last_name'],
    )

    db_user_after_update = user_model.objects.get(id=user.id)

    assert_user_model(
        db_user_after_update,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=payload_update['first_name'],
        last_name=payload_update['last_name'],
    )


def test_update_user_raises_does_not_exist_for_unknown_user(
    repository, payload_update
):
    with pytest.raises(repository.user_model.DoesNotExist):
        repository.update_user(
            user_id=999999,
            user_data=payload_update,
        )


def test_update_user_with_empty_data_returns_same_user(
    repository, user, user_model
):
    user_entity = repository.update_user(user_id=user.id, user_data={})
    db_user_after_update = user_model.objects.get(id=user.id)

    assert_user_entity(
        user_entity,
        user_id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    assert_user_model(
        db_user_after_update,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def test_update_user_raises_value_error_for_not_allowed_fields(
    repository, user
):
    with pytest.raises(ValueError):  # noqa
        repository.update_user(
            user_id=user.id,
            user_data={'is_superuser': True},
        )
