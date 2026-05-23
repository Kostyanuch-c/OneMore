from django.db.models import Q

from apps.problems.dto import SolutionCreateDTO, SolutionUpdateDTO
from apps.problems.exceptions import (
    HiddenSolutionCannotBeMainError,
    MainSolutionCannotBeHiddenError,
    SolutionNotFoundError,
)
from apps.problems.repositories import SolutionRepository


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
        tutor_id: int,
        problem_id: int,
    ) -> int:
        if not self.repository.update_solution(
            solution_id=solution_id,
            dto=dto,
            filters=Q(author_id=tutor_id, problem_id=problem_id),
        ):
            raise SolutionNotFoundError
        return solution_id

    def set_main_solution(self, *, problem_id: int, solution_id: int) -> None:
        is_published = self.repository.get_solution_published_status(
            problem_id=problem_id,
            solution_id=solution_id,
        )
        if is_published is None:
            raise SolutionNotFoundError

        if not is_published:
            raise HiddenSolutionCannotBeMainError

        self.repository.unset_main_solutions(
            problem_id=problem_id,
            exclude_solution_id=solution_id,
        )

        if not self.repository.set_solution_as_main(
            problem_id=problem_id,
            solution_id=solution_id,
        ):
            raise SolutionNotFoundError

    def ensure_solution_can_be_hidden(
        self, *, problem_id: int, solution_id: int, tutor_id: int
    ) -> None:
        if self.repository.exists_main_solution(
            problem_id=problem_id,
            filters=Q(pk=solution_id, author_id=tutor_id),
        ):
            raise MainSolutionCannotBeHiddenError
