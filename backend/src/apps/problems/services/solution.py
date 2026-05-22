from apps.problems.dto import SolutionCreateDTO
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
