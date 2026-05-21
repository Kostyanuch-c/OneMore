from typing import TYPE_CHECKING

from django.db.models import Q

from apps.common.base_entities import Page
from apps.problems.dto import (
    ProblemCreateDTO,
    ProblemFilters,
    ProblemUpdateDTO,
)
from apps.problems.entities import ProblemEntity
from apps.problems.exceptions import ProblemNotFoundError
from apps.problems.repositories import ProblemsRepository
from apps.problems.services.query_builder import ProblemQueryBuilder


if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser, AnonymousUser


class ProblemService:
    repository = ProblemsRepository()
    query_builder = ProblemQueryBuilder()

    def _get_problem_visibility_filters(
        self, user: AbstractUser | AnonymousUser
    ) -> Q:
        if user.is_authenticated and user.is_staff:
            return Q()

        if user.is_authenticated:
            return Q(is_published=True) | Q(author_id=user.pk)

        return Q(is_published=True)

    def _build_problem_list_query(
        self,
        filters: ProblemFilters,
        user: AbstractUser | AnonymousUser,
    ) -> Q:
        return self.query_builder.build(
            filters=filters,
            base_query=self._get_problem_visibility_filters(user),
        )

    def get_problem_detail(
        self, problem_id: int, user: AbstractUser | AnonymousUser
    ) -> ProblemEntity:
        problem = self.repository.get_problem_detail_by_id(
            problem_id=problem_id,
            filters=self._get_problem_visibility_filters(user=user),
        )
        if not problem:
            raise ProblemNotFoundError
        return problem

    def get_problems_page(
        self,
        filters: ProblemFilters,
        limit: int,
        offset: int,
        user: AbstractUser | AnonymousUser,
    ) -> Page[ProblemEntity]:
        query = self._build_problem_list_query(filters=filters, user=user)

        return Page(
            items=self.repository.get_problems_list(
                filters=query,
                limit=limit,
                offset=offset,
            ),
            total=self.repository.get_problems_count(filters=query),
        )

    def create_problem(self, dto: ProblemCreateDTO) -> int:
        return self.repository.create_problem(dto=dto)

    def update_problem(self, problem_id: int, dto: ProblemUpdateDTO) -> int:
        if not self.repository.exists_problem(
            problem_id=problem_id
        ) or not self.repository.update_problem(
            problem_id=problem_id, dto=dto
        ):
            raise ProblemNotFoundError

        return problem_id

    def delete_problem(self, problem_id: int) -> None:
        if not self.repository.delete_problem(problem_id=problem_id):
            raise ProblemNotFoundError
