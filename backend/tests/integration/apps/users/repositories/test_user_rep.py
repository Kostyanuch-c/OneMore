from tests.integration.helpers import assert_user_entity, assert_user_model


def test_create_user(repository, payload_create, user_model):
    created_user = repository.create_user(**payload_create)

    db_user = user_model.objects.get(email=payload_create['email'])

    assert_user_entity(
        created_user,
        user_id=db_user.id,
        email=payload_create['email'],
        username=payload_create['username'],
    )

    assert user_model.objects.count() == 1

    assert_user_model(
        db_user,
        email=payload_create['email'],
        username=payload_create['username'],
        is_active=True,
        is_staff=False,
        has_usable_password=False,
    )
