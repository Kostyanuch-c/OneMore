import logging

from django.db import IntegrityError
from django.db.models import Q

from apps.users.dto import UserFilters, UserUpdateDTO
from apps.users.entities import (
    UserEntity,
)
from apps.users.exceptions.users import (
    EmailAlreadyExistsError,
    UserCreateConflictError,
    UserNameAlreadyExistsError,
)
from apps.users.repositories.user_repository import UserRepository


logger = logging.getLogger('apps.users.service')


class UserService:
    repository = UserRepository()

    @staticmethod
    def _detect_user_conflict_field(exc: IntegrityError) -> str | None:
        cause = exc.__cause__

        diag = getattr(cause, 'diag', None)
        constraint_name = getattr(diag, 'constraint_name', None)
        if constraint_name:
            lowered = constraint_name.lower()
            if 'email' in lowered:
                return 'email'
            if 'username' in lowered:
                return 'username'

        message = str(exc).lower()
        if 'email' in message:
            return 'email'
        if 'username' in message:
            return 'username'

        return None

    def _build_user_query(self, filters: UserFilters) -> Q:
        query = Q()

        if filters.is_active is not None:
            query &= Q(is_active=filters.is_active)

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
        self, filters: UserFilters, limit: int, offset: int
    ) -> list[UserEntity]:
        return self.repository.get_users_list(
            filters=self._build_user_query(filters),
            limit=limit,
            offset=offset,
        )

    def get_user_by_email(
        self, *, email: str, include_inactive: bool = False
    ) -> UserEntity | None:
        return self.repository.get_user_by_email(
            email=email, include_inactive=include_inactive
        )

    def create_user(self, username: str, email: str) -> UserEntity:
        try:
            return self.repository.create_user(
                username=username,
                email=email,
            )
        except IntegrityError as e:
            field = self._detect_user_conflict_field(e)

            if field == 'email':
                logger.warning('User create conflict | field=email')
                raise EmailAlreadyExistsError from e

            if field == 'username':
                logger.warning('User create conflict | field=username')
                raise UserNameAlreadyExistsError from e

            logger.exception(
                'User create failed with integrity error | field=%s',
                field or 'unknown',
            )
            raise UserCreateConflictError from e

    def update_user(
        self,
        user_id: int,
        user_data: UserUpdateDTO,
    ) -> UserEntity:

        try:
            return self.repository.update_user(
                user_id=user_id,
                user_data=user_data,
            )
        except IntegrityError as e:
            if user_data.username:
                logger.warning(
                    'User update conflict | user_id=%s field=username',
                    user_id,
                )
                raise UserNameAlreadyExistsError from e
            logger.exception(
                'User update failed with integrity error | user_id=%s field=unknown',
                user_id,
            )
            raise
