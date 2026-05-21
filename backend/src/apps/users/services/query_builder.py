from apps.common.base_query_builder import BaseQueryBuilder
from apps.users.dto import UserFilters


class UserQueryBuilder(BaseQueryBuilder[UserFilters]):
    FILTER_LOOKUPS = {
        'is_active': 'is_active',
        'created_from': 'date_joined__gte',
        'created_to': 'date_joined__lte',
    }

    SEARCH_FIELDS = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
