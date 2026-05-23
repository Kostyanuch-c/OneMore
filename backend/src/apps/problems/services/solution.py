from typing import TYPE_CHECKING

from django.db.models import Q

from apps.problems.dto import SolutionCreateDTO, SolutionUpdateDTO
from apps.problems.exceptions import SolutionNotFoundError
from apps.problems.repositories import SolutionRepository


if TYPE_CHECKING:
    from apps.users.models import User


class SolutionService:
    repository = SolutionRepository()

    def create_solution(self, *, dto: SolutionCreateDTO) -> int:
        is_main = not self.repository.exists_main_solution(
            problem_id=dto.problem_id,
        )

        return self.repository.create_solution(
            dto=dto,
            is_main=is_main,
        )

    def update_solution(
        self,
        *,
        solution_id: int,
        dto: SolutionUpdateDTO,
        user: User,
        problem_id: int,
    ) -> int:
        if not self.repository.update_solution(
            solution_id=solution_id,
            dto=dto,
            filters=Q(author_id=user.pk, problem_id=problem_id),
        ):
            raise SolutionNotFoundError
        return solution_id

    def set_main_solution(self, *, problem_id: int, solution_id: int) -> None:
        self.repository.unset_main_solutions(
            problem_id=problem_id,
            exclude_solution_id=solution_id,
        )

        if not self.repository.set_solution_as_main(
            problem_id=problem_id,
            solution_id=solution_id,
        ):
            raise SolutionNotFoundError
