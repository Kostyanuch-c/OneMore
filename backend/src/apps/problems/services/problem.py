from typing import TYPE_CHECKING

from django.db.models import Q

from apps.common.base_entities import Page
from apps.problems.dto import (
    ProblemCreateDTO,
    ProblemUpdateDTO,
    ProfileProblemFilters,
    PublicProblemFilters,
)
from apps.problems.entities import ProblemEntity
from apps.problems.enums import PublicationStatus
from apps.problems.exceptions import ProblemNotFoundError
from apps.problems.repositories import ProblemsRepository
from apps.problems.services.query_builder import ProblemQueryBuilder


if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser

    from apps.users.models import User


class ProblemService:
    repository = ProblemsRepository()
    query_builder = ProblemQueryBuilder()

    def _get_public_solution_filters(self, *, user: User | AnonymousUser) -> Q:
        # For demonstration solutions for author where a solution not is_published
        public_query = Q(is_published=True)

        if user.is_authenticated and user.is_tutor:
            return public_query | Q(author_id=user.pk)

        return public_query

    def _needs_distinct(
        self, filters: PublicProblemFilters | ProfileProblemFilters
    ) -> bool:
        return bool(filters.tag_ids)

    def _get_problems_page(
        self,
        *,
        filters: PublicProblemFilters | ProfileProblemFilters,
        base_query: Q,
        limit: int,
        offset: int,
    ) -> Page[ProblemEntity]:
        query = self.query_builder.build(
            filters=filters,
            base_query=base_query,
        )

        distinct = self._needs_distinct(filters=filters)

        return Page(
            items=self.repository.get_problems_list(
                filters=query,
                limit=limit,
                offset=offset,
                distinct=distinct,
            ),
            total=self.repository.get_problems_count(
                filters=query,
                distinct=distinct,
            ),
        )

    def _lock_problem_for_update(self, *, problem_id: int, filters: Q) -> None:
        if not self.repository.exists_problem_for_update(
            problem_id=problem_id,
            filters=filters,
        ):
            raise ProblemNotFoundError

    def get_public_problem_detail(
        self, *, problem_id: int, user: User | AnonymousUser
    ) -> ProblemEntity:
        problem = self.repository.get_problem_detail_by_id(
            problem_id=problem_id,
            filters=Q(status=PublicationStatus.PUBLISHED),
            with_solutions=True,
            solution_filters=self._get_public_solution_filters(user=user),
        )

        if problem is None:
            raise ProblemNotFoundError

        return problem

    def get_public_problems_page(
        self, *, filters: PublicProblemFilters, limit: int, offset: int
    ) -> Page[ProblemEntity]:
        return self._get_problems_page(
            filters=filters,
            base_query=Q(status=PublicationStatus.PUBLISHED),
            limit=limit,
            offset=offset,
        )

    def get_my_problem_detail(
        self, *, problem_id: int, user: User
    ) -> ProblemEntity:
        problem = self.repository.get_problem_detail_by_id(
            problem_id=problem_id,
            filters=Q(author_id=user.pk),
            with_solutions=True,
            solution_filters=None,
        )

        if problem is None:
            raise ProblemNotFoundError

        return problem

    def get_my_problems_page(
        self,
        *,
        filters: ProfileProblemFilters,
        limit: int,
        offset: int,
        user: User,
    ) -> Page[ProblemEntity]:
        return self._get_problems_page(
            filters=filters,
            base_query=Q(author_id=user.pk),
            limit=limit,
            offset=offset,
        )

    def create_problem(self, *, dto: ProblemCreateDTO) -> int:
        return self.repository.create_problem(dto=dto)

    def update_problem(
        self, *, problem_id: int, dto: ProblemUpdateDTO, user: User
    ) -> int:
        if not self.repository.update_problem(
            problem_id=problem_id, dto=dto, filters=Q(author_id=user.pk)
        ):
            raise ProblemNotFoundError

        return problem_id

    def delete_my_problem(self, *, problem_id: int, user: User) -> None:
        if not self.repository.delete_problem(
            problem_id=problem_id,
            filters=Q(author_id=user.pk),
        ):
            raise ProblemNotFoundError

    def lock_problem_available_for_solution_create(
        self, *, problem_id: int, author_id: int
    ) -> None:
        self._lock_problem_for_update(
            problem_id=problem_id,
            filters=(
                Q(status=PublicationStatus.PUBLISHED) | Q(author_id=author_id)
            ),
        )

    def lock_my_problem_for_update(
        self, *, problem_id: int, tutor_id: int
    ) -> None:
        self._lock_problem_for_update(
            problem_id=problem_id,
            filters=Q(author_id=tutor_id),
        )
