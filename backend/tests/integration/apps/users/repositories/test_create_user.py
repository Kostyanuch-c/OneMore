from django.db import IntegrityError

import pytest

from tests.integration.helpers import (
    assert_user_entity_and_model,
)


def test_create_user_success(repository, payload_create, user_model):
    created_user = repository.create_user(**payload_create)

    db_user = user_model.objects.get(email=payload_create['email'])

    assert user_model.objects.count() == 1

    assert_user_entity_and_model(
        user_entity=created_user,
        db_user=db_user,
        user_id=db_user.id,
        email=payload_create['email'],
        username=payload_create['username'],
    )


@pytest.mark.parametrize('conflict_field', ['email', 'username'])
def test_create_user_raises_integrity_error_on_unique_conflict(
    repository,
    user,
    conflict_field,
):
    payload = {
        'email': 'new_test_user@example.com',
        'username': 'new_test_user',
    }

    if conflict_field == 'email':
        payload['email'] = user.email
    else:
        payload['username'] = user.username

    with pytest.raises(IntegrityError):
        repository.create_user(**payload)


@pytest.mark.parametrize(
    ('email', 'username'),
    [
        (None, 'new_test_user'),
        ('new_test_user@example.com', None),
    ],
)
def test_create_user_raises_integrity_error_on_null_values(
    repository,
    email,
    username,
):
    with pytest.raises(IntegrityError):
        repository.create_user(email=email, username=username)
