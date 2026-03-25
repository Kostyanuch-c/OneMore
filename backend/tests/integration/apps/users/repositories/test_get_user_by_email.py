from tests.integration.helpers import (
    assert_user_entity,
    serialize_users_for_snapshot,
)


def test_get_user_by_email_returns_user_entity(
    repository, user, user_factory, user_model
):
    found_user = repository.get_user_by_email(email=user.email)

    assert_user_entity(
        found_user,
        user_id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
    )


def test_get_user_by_email_returns_none_when_user_not_found(
    repository, user, user_model
):
    found_user = repository.get_user_by_email(email='missing_Email')

    assert found_user is None


def test_get_user_by_email_does_not_return_inactive_user_by_default(
    repository,
    user_factory,
):
    inactive_user = user_factory(is_active=False)

    found_user = repository.get_user_by_email(email=inactive_user.email)

    assert found_user is None


def test_get_user_by_email_returns_inactive_user_when_include_inactive_true(
    repository,
    user_factory,
    user_model,
):
    inactive_user = user_factory(is_active=False)

    found_user = repository.get_user_by_email(
        email=inactive_user.email,
        include_inactive=True,
    )

    assert_user_entity(
        found_user,
        user_id=inactive_user.id,
        email=inactive_user.email,
        username=inactive_user.username,
        is_active=inactive_user.is_active,
        is_staff=inactive_user.is_staff,
    )


def test_get_user_by_email_is_case_insensitive(repository, user):
    found_user = repository.get_user_by_email(email=user.email.upper())

    assert_user_entity(
        found_user,
        user_id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
    )


def test_get_user_by_email_does_not_change_db_state(
    repository,
    user,
    user_factory,
    user_model,
):
    user_factory.create_batch(3)
    user_factory.create_batch(3, is_active=False)

    before = serialize_users_for_snapshot(user_model)
    repository.get_user_by_email(email=user.email)

    after = serialize_users_for_snapshot(user_model)

    assert len(after) == len(before)
    assert after == before
