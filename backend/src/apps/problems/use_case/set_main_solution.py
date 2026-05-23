from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db import transaction

from apps.common import BaseUseCase
from apps.problems.dto import SolutionMutationResult
from apps.problems.services import ProblemService
from apps.problems.services.solution import SolutionService


if TYPE_CHECKING:
    from apps.users.models import User


@dataclass
class SetMainSolutionUseCase(BaseUseCase[SolutionMutationResult]):
    problem_service: ProblemService
    solution_service: SolutionService
    problem_id: int
    solution_id: int
    user: User

    @transaction.atomic()
    def act(self) -> SolutionMutationResult:
        self.problem_service.lock_my_problem_for_update(
            problem_id=self.problem_id,
            user=self.user,
        )

        self.solution_service.set_main_solution(
            problem_id=self.problem_id,
            solution_id=self.solution_id,
        )

        return SolutionMutationResult(
            problem_id=self.problem_id,
            solution_id=self.solution_id,
            detail_url=f'problems/{self.problem_id}/solutions/{self.solution_id}',
        )
