from typing import TYPE_CHECKING

from django.db.models import Q

from apps.common.base_entities import Page
from apps.problems.dto import (
    ProblemCreateDTO,
    ProblemFilters,
    ProblemUpdateDTO,
)
from apps.problems.entities import ProblemEntity
from apps.problems.enums import PublicationStatus
from apps.problems.exceptions import ProblemNotFoundError
from apps.problems.repositories import ProblemsRepository
from apps.problems.services.query_builder import ProblemQueryBuilder


if TYPE_CHECKING:
    from apps.users.models import User


class ProblemService:
    repository = ProblemsRepository()
    query_builder = ProblemQueryBuilder()

    def get_public_problem_detail(self, *, problem_id: int) -> ProblemEntity:
        problem = self.repository.get_problem_detail_by_id(
            problem_id=problem_id,
            filters=Q(status=PublicationStatus.PUBLISHED),
            with_solutions=True,
            solution_filters=Q(is_published=True),
        )

        if problem is None:
            raise ProblemNotFoundError

        return problem

    def get_public_problems_page(
        self, *, filters: ProblemFilters, limit: int, offset: int
    ) -> Page[ProblemEntity]:
        query = self.query_builder.build(
            filters=filters,
            base_query=Q(status=PublicationStatus.PUBLISHED),
        )

        return Page(
            items=self.repository.get_problems_list(
                filters=query,
                limit=limit,
                offset=offset,
            ),
            total=self.repository.get_problems_count(filters=query),
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
        self, *, filters: ProblemFilters, limit: int, offset: int, user: User
    ) -> Page[ProblemEntity]:
        query = self.query_builder.build(
            filters=filters,
            base_query=Q(author_id=user.pk),
        )

        return Page(
            items=self.repository.get_problems_list(
                filters=query,
                limit=limit,
                offset=offset,
            ),
            total=self.repository.get_problems_count(filters=query),
        )

    def create_problem(self, *, dto: ProblemCreateDTO) -> int:
        return self.repository.create_problem(dto=dto)

    def update_problem(
        self, *, problem_id: int, dto: ProblemUpdateDTO, user: User
    ) -> int:
        if not self.repository.exists_problem(
            problem_id=problem_id,
            filters=Q(author_id=user.pk),
        ) or not self.repository.update_problem(
            problem_id=problem_id, dto=dto
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
        self, *, problem_id: int, user: User
    ) -> None:
        if not self.repository.exists_problem_for_update(
            problem_id=problem_id,
            filters=Q(status=PublicationStatus.PUBLISHED)
            | Q(author_id=user.pk),
        ):
            raise ProblemNotFoundError
