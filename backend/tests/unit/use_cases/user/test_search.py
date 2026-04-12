from apps.common.base_entities import Page
from apps.users.dto import UserFilters
from apps.users.use_cases import SearchUsers


def test_use_case_search_user_calls_service(user_service, mocker, user_entity):
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

    get_users_list_mock = mocker.patch.object(
        user_service,
        'get_users_list',
        return_value=user_list,
    )

    get_users_count_mock = mocker.patch.object(
        user_service,
        'get_users_count',
        return_value=total,
    )

    result = SearchUsers(
        service=user_service,
        filters=filters,
        limit=limit,
        offset=offset,
    )()

    get_users_list_mock.assert_called_once_with(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    get_users_count_mock.assert_called_once_with(
        filters=filters,
    )

    assert result == expected
