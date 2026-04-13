from apps.common.base_entities import Page
from apps.users.dto import UserFilters
from apps.users.use_cases import SearchUsers


def test_use_case_search_user_calls_service(user_service_mock, user_entity):
    user_list, total = (
        [user_entity],
        10,
    )
    limit, offset = 10, 0
    filters = UserFilters(is_active=True)
    expected = Page(
        items=user_list,
        total=total,
    )

    user_service_mock.get_users_list.return_value = user_list
    user_service_mock.get_users_count.return_value = total

    result = SearchUsers(
        service=user_service_mock,
        filters=filters,
        limit=limit,
        offset=offset,
    )()

    user_service_mock.get_users_list.assert_called_once_with(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    user_service_mock.get_users_count.assert_called_once_with(
        filters=filters,
    )

    assert result == expected
