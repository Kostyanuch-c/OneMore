from apps.common.base_entities import Page
from apps.users.dto import UserFilters
from apps.users.use_cases import SearchUsers


def test_search_user_happy_path_with_pagination_active_users(
    users,
    user_service,
):
    offset, limit = 2, 5

    filters = UserFilters(is_active=True)

    expected_source = [user for user in users if user.is_active]
    expected_total = len(expected_source)
    expected_users = expected_source[offset : offset + limit]

    result = SearchUsers(
        service=user_service,
        filters=filters,
        offset=offset,
        limit=limit,
    )()

    assert isinstance(result, Page)
    assert result.total == expected_total
    assert [user.id for user in result.items] == [
        user.id for user in expected_users
    ]
