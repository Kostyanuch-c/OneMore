from collections.abc import Callable
from functools import wraps
from typing import Any, Concatenate

from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404

from apps.common.utils import constraint_name
from apps.users.entities import (
    UserEntity,
)
from apps.users.excepions.users import (
    EmailAlreadyExistsError,
    UserNameAlreadyExistsError,
)
from apps.users.filters import UserFilters
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository


def map_user_integrity_errors[**P, R](
    method: Callable[Concatenate[UserService, P], R],
) -> Callable[Concatenate[UserService, P], R]:
    @wraps(method)
    def wrapper(self: UserService, *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return method(self, *args, **kwargs)
        except IntegrityError as e:
            cname = constraint_name(e)
            if cname == self.repository.USERNAME_CONSTRAINT:
                raise UserNameAlreadyExistsError from e
            if cname == self.repository.EMAIL_CONSTRAINT:
                raise EmailAlreadyExistsError from e
            raise

    return wrapper  # type: ignore


class UserService:
    repository = UserRepository()

    def _build_user_query(self, filters: UserFilters) -> Q:
        query = Q(is_active=filters.is_active)

        if filters.search:
            query &= (
                Q(username__icontains=filters.search)
                | Q(email__icontains=filters.search)
                | Q(first_name__icontains=filters.search)
                | Q(last_name__icontains=filters.search)
            )
        if filters.created_from:
            query &= Q(date_joined__gte=filters.created_from)

        if filters.created_to:
            query &= Q(date_joined__lte=filters.created_to)
        return query

    def get_users_count(self, filters: UserFilters) -> int:
        return self.repository.get_users_count(
            filters=self._build_user_query(filters)
        )

    def get_users_list(
        self, filters: UserFilters, offset: int, limit: int
    ) -> list[UserEntity]:
        return self.repository.get_users_list(
            filters=self._build_user_query(filters),
            offset=offset,
            limit=limit,
        )

    def get_all_objects(self) -> list[UserEntity]:
        return self.repository.get_all_users()

    def get_user(self, user_id: int) -> UserEntity:
        try:
            return self.repository.get_user_by_id(user_id)
        except User.DoesNotExist:
            raise Http404

    @map_user_integrity_errors
    def create_user(
        self,
        password: str,
        username: str,
        email: str | None = None,
    ) -> UserEntity:

        return self.repository.create_user(
            password=password,
            username=username,
            email=email,
        )

    @map_user_integrity_errors
    def update_user(
        self,
        user_id: int,
        user_data: dict[
            str, Any
        ],  # подумать как про типизировать даже когда появится токе
    ) -> UserEntity:

        return self.repository.update_user(
            user_id=user_id, user_data=user_data
        )

    def delete_user(self, user_id: int) -> None:

        return self.repository.delete_object(user_id)
