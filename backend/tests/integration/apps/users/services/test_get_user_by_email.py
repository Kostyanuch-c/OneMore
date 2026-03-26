import pytest

from tests.integration.helpers import assert_user_entity


@pytest.mark.parametrize(
    ('is_active', 'include_inactive', 'should_return_user'),
    [
        (True, False, True),
        (True, True, True),
        (False, False, False),
        (False, True, True),
    ],
)
def test_get_user_by_email_returns_expected_user_depends_on_include_inactive(
    user_factory,
    user_model,
    payload_create_user,
    user_service,
    is_active,
    include_inactive,
    should_return_user,
):
    email = payload_create_user['email']
    username = payload_create_user['username']

    user_factory.create(
        is_active=is_active,
        email=email,
        username=username,
    )

    user_entity = user_service.get_user_by_email(
        email=email,
        include_inactive=include_inactive,
    )

    if not should_return_user:
        assert user_entity is None
    else:
        assert_user_entity(
            user_entity,
            email=email,
            username=username,
            is_active=is_active,
        )

    assert user_model.objects.count() == 1


def test_get_user_by_email_returns_none_when_user_not_found(user_service):
    user_entity = user_service.get_user_by_email(email='missing@example.com')

    assert user_entity is None
