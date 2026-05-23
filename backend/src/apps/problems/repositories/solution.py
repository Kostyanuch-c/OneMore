from django.db.models import Q
from django.utils import timezone

from apps.problems.dto import SolutionCreateDTO, SolutionUpdateDTO
from apps.problems.models import Solution


class SolutionRepository:
    model = Solution

    def exists_main_solution(
        self, *, problem_id: int, filters: Q | None = None
    ) -> bool:
        return self.model.objects.filter(
            filters or Q(),
            problem_id=problem_id,
            is_main=True,
        ).exists()

    def unset_main_solutions(
        self, *, problem_id: int, exclude_solution_id: int | None = None
    ) -> None:
        queryset = self.model.objects.filter(
            problem_id=problem_id,
            is_main=True,
        )

        if exclude_solution_id is not None:
            queryset = queryset.exclude(pk=exclude_solution_id)

        queryset.update(
            is_main=False,
            updated_at=timezone.now(),
        )

    def set_solution_as_main(
        self, *, problem_id: int, solution_id: int
    ) -> bool:
        updated_count = self.model.objects.filter(
            pk=solution_id,
            problem_id=problem_id,
        ).update(
            is_main=True,
            updated_at=timezone.now(),
        )

        return updated_count > 0

    def create_solution(self, *, dto: SolutionCreateDTO, is_main: bool) -> int:
        solution = self.model.objects.create(
            problem_id=dto.problem_id,
            author_id=dto.author_id,
            name=dto.name,
            content=dto.content,
            is_published=dto.is_published,
            is_main=is_main,
        )

        return solution.id

    def update_solution(
        self,
        *,
        solution_id: int,
        dto: SolutionUpdateDTO,
        filters: Q | None = None,
    ) -> bool:
        update_data = {
            **dto.data,
            'updated_at': timezone.now(),
        }

        updated_count = self.model.objects.filter(
            filters or Q(), pk=solution_id
        ).update(**update_data)

        return updated_count > 0
