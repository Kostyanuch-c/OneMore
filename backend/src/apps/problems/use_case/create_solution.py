from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db import transaction

from apps.common import BaseUseCase
from apps.problems.dto import SolutionCreateDTO, SolutionMutationResult
from apps.problems.services import ProblemService
from apps.problems.services.solution import SolutionService


if TYPE_CHECKING:
    from apps.users.models import User


@dataclass
class CreateSolutionUseCase(BaseUseCase[SolutionMutationResult]):
    problem_service: ProblemService
    solution_service: SolutionService
    create_data: SolutionCreateDTO
    user: User

    @transaction.atomic()
    def act(self) -> SolutionMutationResult:
        # transaction because we need to block the problem,
        self.problem_service.lock_problem_available_for_solution_create(
            problem_id=self.create_data.problem_id,
            user=self.user,
        )

        solution_id = self.solution_service.create_solution(
            dto=self.create_data,
        )

        return SolutionMutationResult(
            problem_id=self.create_data.problem_id,
            solution_id=solution_id,
            detail_url=(
                f'problems/{self.create_data.problem_id}/solutions/{solution_id}'
            ),
        )
