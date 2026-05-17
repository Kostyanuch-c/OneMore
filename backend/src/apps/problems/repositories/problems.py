from django.db.models import Q
from django.utils import timezone

from apps.problems.dto import ProblemCreateDTO, ProblemUpdateDTO
from apps.problems.entities import ProblemEntity
from apps.problems.models import Problem, Solution
from apps.problems.repositories.converters import ProblemConverter


class ProblemsRepository:
    model = Problem
    solution_model = Solution
    converter = ProblemConverter

    def exists_problem(self, problem_id: int) -> bool:
        return self.model.objects.filter(pk=problem_id).exists()

    def get_problem_detail_by_id(
        self,
        *,
        problem_id: int,
        filters: Q | None = None,
        with_solutions: bool = True,
    ) -> ProblemEntity | None:
        queryset = self.model.objects.for_detail(
            with_solutions=with_solutions,
        ).filter(pk=problem_id)

        if filters is not None:
            queryset = queryset.filter(filters)

        problem = queryset.first()

        if problem is None:
            return None

        return self.converter.to_entity(
            problem,
            with_solutions=with_solutions,
        )

    def create_problem(self, dto: ProblemCreateDTO) -> int:
        # transaction we not use because we opened the transaction in the use case
        problem = self.model.objects.create(
            title=dto.title,
            question=dto.question,
            difficulty=dto.difficulty,
            source=dto.source,
            topic_id=dto.topic_id,
            author_id=dto.author_id,
            is_published=dto.is_published,
        )

        if dto.tag_ids:
            problem.tags.add(*dto.tag_ids)

        return problem.pk

    def update_problem(
        self,
        problem_id: int,
        dto: ProblemUpdateDTO,
    ) -> bool:
        update_data = dto.data.copy()
        tag_ids = update_data.pop('tag_ids', None)

        update_data['updated_at'] = timezone.now()

        updated_count = self.model.objects.filter(pk=problem_id).update(
            **update_data
        )

        if updated_count == 0:
            return False

        if tag_ids is not None:
            problem = self.model.objects.filter(pk=problem_id).first()

            if problem is None:
                return False

            problem.tags.set(tag_ids)

        return True

    def delete_problem(self, problem_id: int) -> bool:
        deleted_count, _ = self.model.objects.filter(pk=problem_id).delete()
        return deleted_count > 0
