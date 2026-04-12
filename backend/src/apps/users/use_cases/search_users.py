from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.common.base_entities import Page
from apps.users.dto import UserFilters
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class SearchUsers(BaseUseCase[Page[UserEntity]]):
    service: UserService
    filters: UserFilters
    offset: int
    limit: int

    def act(self) -> Page[UserEntity]:
        return Page(
            items=self.service.get_users_list(
                filters=self.filters,
                limit=self.limit,
                offset=self.offset,
            ),
            total=self.service.get_users_count(filters=self.filters),
        )
