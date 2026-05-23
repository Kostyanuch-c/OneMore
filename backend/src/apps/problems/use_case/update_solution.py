from collections.abc import Callable
from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.common.exception import EmptyUpdateDataError
from apps.problems.dto import (
    SolutionMutationResult,
    SolutionUpdateDTO,
)
from apps.problems.services import ProblemService
from apps.problems.services.solution import SolutionService


@dataclass
class UpdateSolutionUseCase(BaseUseCase[SolutionMutationResult]):
    problem_service: ProblemService
    solution_service: SolutionService
    update_data: SolutionUpdateDTO
    problem_id: int
    solution_id: int
    tutor_id: int

    def act(self) -> SolutionMutationResult:
        solution_id = self.solution_service.update_solution(
            dto=self.update_data,
            solution_id=self.solution_id,
            tutor_id=self.tutor_id,
            problem_id=self.problem_id,
        )

        return SolutionMutationResult(
            problem_id=self.problem_id,
            solution_id=solution_id,
            detail_url=(f'problems/{self.problem_id}/solutions/{solution_id}'),
        )

    def get_validators(self) -> list[Callable[[], None]]:
        return [
            self.validate_empty_update_data,
        ]

    def validate_empty_update_data(self) -> None:
        if not self.update_data.data:
            raise EmptyUpdateDataError

    def validate_can_hide_solution(self) -> None:
        # You can't hide the main solution
        if self.update_data.data.get('is_published') is not False:
            return

        self.solution_service.ensure_solution_can_be_hidden(
            solution_id=self.solution_id,
            problem_id=self.problem_id,
            tutor_id=self.tutor_id,
        )
