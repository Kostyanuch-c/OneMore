from django.db.models import Q

from apps.problems.dto import ProblemCreateDTO, ProblemUpdateDTO
from apps.problems.entities import ProblemEntity, ProblemMutationEntity
from apps.problems.models import Problem, Solution
from apps.problems.repositories.converters import ProblemConverter


class ProblemsRepository:
    model = Problem
    solution_model = Solution
    converter = ProblemConverter

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

    def create_problem(self, dto: ProblemCreateDTO) -> ProblemMutationEntity:
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

        return ProblemMutationEntity(
            id=problem.pk,
            title=problem.title,
        )

    def update_problem(
        self,
        problem_id: int,
        dto: ProblemUpdateDTO,
    ) -> ProblemMutationEntity | None:
        problem = self.model.objects.filter(pk=problem_id).first()

        if problem is None:
            return None

        update_data = dto.data.copy()
        tag_ids = update_data.pop('tag_ids', None)

        for field, value in update_data.items():
            setattr(problem, field, value)

        if update_data:
            problem.save(update_fields=list(update_data.keys()))

        if 'tag_ids' in update_data:
            problem.tags.set(tag_ids)

        return ProblemMutationEntity(
            id=problem.pk,
            title=problem.title,
        )
