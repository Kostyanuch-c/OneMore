from apps.problems.dto import SolutionCreateDTO
from apps.problems.models import Solution


class SolutionRepository:
    model = Solution

    def exists_main_solution(self, *, problem_id: int) -> bool:
        return self.model.objects.filter(
            problem_id=problem_id,
            is_main=True,
        ).exists()

    def unset_main_solutions(self, *, problem_id: int) -> None:
        self.model.objects.filter(
            problem_id=problem_id,
            is_main=True,
        ).update(is_main=False)

    def create_solution(
        self,
        *,
        dto: SolutionCreateDTO,
        is_main: bool,
    ) -> int:
        solution = self.model.objects.create(
            problem_id=dto.problem_id,
            author_id=dto.author_id,
            name=dto.name,
            content=dto.content,
            is_published=dto.is_published,
            is_main=is_main,
        )

        return solution.id
