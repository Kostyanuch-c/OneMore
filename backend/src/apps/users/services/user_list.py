from collections.abc import Callable
from dataclasses import dataclass

from django.db.models import Q

from apps.common.base_exeption import ApplicationError
from apps.common.base_service import BaseService
from apps.users.entities import UserEntity
from apps.users.filters import UserFilters
from apps.users.repositories.user_repository import UserRepository


@dataclass
class UsersPage[Entity]:
    items: list[Entity]
    total: int


@dataclass
class UsersListCount(BaseService):
    repo: UserRepository
    filters: UserFilters
    offset: int
    limit: int

    def _build_user_query(self) -> Q:
        query = Q(is_active=self.filters.is_active)

        if self.filters.search:
            query &= (
                Q(username__icontains=self.filters.search)
                | Q(email__icontains=self.filters.search)
                | Q(first_name__icontains=self.filters.search)
                | Q(last_name__icontains=self.filters.search)
            )
        if self.filters.created_from:
            query &= Q(date_joined__gte=self.filters.created_from)

        if self.filters.created_to:
            query &= Q(date_joined__lte=self.filters.created_to)

        return query

    def act(self) -> UsersPage[UserEntity]:
        query = self._build_user_query()
        return UsersPage(
            items=self.repo.get_users_list(
                filters=query,
                offset=self.offset,
                limit=self.limit,
            ),
            total=self.repo.get_users_count(filters=query),
        )

    def get_validators(self) -> list[Callable[[], None]]:
        return [self.validate_time_filter]

    def validate_time_filter(self) -> None:
        if self.filters.created_from and self.filters.created_to:  # noqa: SIM102
            if self.filters.created_from > self.filters.created_to:
                raise ApplicationError(
                    message='created_from must be less than created_to',
                    status_code=400,
                )
