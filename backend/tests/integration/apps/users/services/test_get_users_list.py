import pytest

from apps.users.dto import UserFilters
from apps.users.entities import UserEntity


@pytest.mark.parametrize(
    ('is_active', 'limit', 'offset', 'expected_count'),
    [
        (None, 15, 0, 15),
        (None, 4, 0, 4),
        (None, 5, 5, 5),
        (False, 15, 0, 10),
        (True, 5, 0, 5),
    ],
)
def test_get_users_list_returns_expected_users(
    user_service,
    users,
    user_model,
    is_active,
    limit,
    offset,
    expected_count,
):
    filters = UserFilters(is_active=is_active)

    expected_source = users
    if is_active is not None:
        expected_source = [
            user for user in users if user.is_active is is_active
        ]

    expected_users = expected_source[offset : offset + limit]

    users_list = user_service.get_users_list(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    assert len(users_list) == expected_count
    assert all(isinstance(user, UserEntity) for user in users_list)
    assert [user.id for user in users_list] == [
        user.id for user in expected_users
    ]
    assert user_model.objects.count() == len(users)


def test_get_users_list_returns_empty_list_when_no_users_match(
    user_service, users
):
    users_list = user_service.get_users_list(
        filters=UserFilters(search='missing@example.com', is_active=False),
        limit=10,
        offset=0,
    )

    assert users_list == []
