from typing import TYPE_CHECKING

from django.db.models import Q

from apps.problems.dto import ProblemCreateDTO
from apps.problems.entities import ProblemCreatedEntity, ProblemEntity
from apps.problems.exceptions import ProblemNotFoundError
from apps.problems.repositories import ProblemsRepository


if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser, AnonymousUser


class ProblemService:
    repository = ProblemsRepository()

    def _get_problem_visibility_filters(
        self, user: AbstractUser | AnonymousUser
    ) -> Q:
        if user.is_authenticated and user.is_staff:
            return Q()

        if user.is_authenticated:
            return Q(is_published=True) | Q(author_id=user.pk)

        return Q(is_published=True)

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

    def create_problem(self, dto: ProblemCreateDTO) -> ProblemCreatedEntity:
        return self.repository.create_problem(dto=dto)
