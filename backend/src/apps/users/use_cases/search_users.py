from dataclasses import dataclass

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
    offset: int
    limit: int

    def act(self) -> UsersPage[UserEntity]:
        return UsersPage(
            items=self.service.get_users_list(
                filters=self.filters,
                offset=self.offset,
                limit=self.limit,
            ),
            total=self.service.get_users_count(filters=self.filters),
        )
