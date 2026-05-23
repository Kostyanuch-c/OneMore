from dataclasses import dataclass

from django.db import transaction

from apps.common import BaseUseCase
from apps.problems.dto import SolutionCreateDTO, SolutionMutationResult
from apps.problems.services import ProblemService
from apps.problems.services.solution import SolutionService


@dataclass
class CreateSolutionUseCase(BaseUseCase[SolutionMutationResult]):
    problem_service: ProblemService
    solution_service: SolutionService
    create_data: SolutionCreateDTO

    @transaction.atomic()
    def act(self) -> SolutionMutationResult:
        # transaction because we need to block the problem,
        self.problem_service.lock_problem_available_for_solution_create(
            problem_id=self.create_data.problem_id,
            author_id=self.create_data.author_id,
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
