import pytest

from tests.integration.helpers import assert_user_entity_and_model

from apps.users.excepions.users import (
    EmailAlreadyExistsError,
    UserNameAlreadyExistsError,
)


def test_create_user_success(
    user_service, payload_create, user_factory, user_model
):
    email, username = payload_create['email'], payload_create['username']

    user_entity = user_service.create_user(**payload_create)

    db_user = user_model.objects.get(email=email)

    assert_user_entity_and_model(
        user_entity=user_entity,
        db_user=db_user,
        user_id=db_user.id,
        email=email,
        username=username,
    )

    assert user_model.objects.count() == 1


@pytest.mark.parametrize(
    ('conflict_field', 'expected_exception'),
    [
        ('email', EmailAlreadyExistsError),
        ('username', UserNameAlreadyExistsError),
    ],
)
def test_create_user_already_exists_raises_custom_error(
    user_service,
    user,
    conflict_field,
    expected_exception,
):
    payload = {
        'email': 'new_test_user@example.com',
        'username': 'new_test_user',
    }

    if conflict_field == 'email':
        payload['email'] = user.email
    else:
        payload['username'] = user.username

    with pytest.raises(expected_exception):
        user_service.create_user(**payload)
