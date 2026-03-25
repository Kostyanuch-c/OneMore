from django.db.models import Q

from apps.users.entities import UserEntity


def test_get_users_list_returns_all_users_with_empty_filters_and_full_limit(
    repository, user_factory, user_model
):
    user_factory.create_batch(5)
    user_factory.create_batch(5, is_active=False)

    users = repository.get_users_list(filters=Q(), limit=10, offset=0)

    assert len(users) == user_model.objects.count()
    assert all(isinstance(user, UserEntity) for user in users)


def test_get_users_list_applies_limit(repository, user_factory):
    limit = 4
    user_factory.create_batch(10)

    users = repository.get_users_list(filters=Q(), limit=limit, offset=0)

    assert len(users) == limit


def test_get_users_list_applies_offset(repository, user_factory):
    created_users = user_factory.create_batch(15)

    expected_users = sorted(
        created_users,
        key=lambda user: user.date_joined,
        reverse=True,
    )[5:10]

    users = repository.get_users_list(filters=Q(), limit=5, offset=5)

    assert [user.id for user in users] == [user.id for user in expected_users]


def test_get_users_list_applies_filters(repository, user_factory):
    user_factory.create_batch(3, is_active=True)
    user_factory.create_batch(4, is_active=False)

    users = repository.get_users_list(
        filters=Q(is_active=False), limit=10, offset=0
    )

    assert len(users) == 4  # noqa
    assert all(user.is_active is False for user in users)


def test_get_users_list_returns_empty_list_when_no_users_match(
    repository, user_factory
):
    user_factory.create_batch(3, is_active=False)
    users = repository.get_users_list(
        filters=Q(email='missing.email.com') & Q(is_active=False),
        limit=10,
        offset=0,
    )

    assert users == []
