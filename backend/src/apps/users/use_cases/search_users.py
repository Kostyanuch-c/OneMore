from dataclasses import dataclass

from api.filters import PaginationIn
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.filters import UserFilters
from apps.users.services import UserService


@dataclass
class UsersPage[Entity]:
    items: list[Entity]
    total: int


@dataclass
class SearchUsers(BaseUseCase):
    service: UserService
    filters: UserFilters
    pagination: PaginationIn

    def act(self) -> UsersPage[UserEntity]:
        return UsersPage(
            items=self.service.get_users_list(
                filters=self.filters,
                offset=self.pagination.offset,
                limit=self.pagination.limit,
            ),
            total=self.service.get_users_count(filters=self.filters),
        )
