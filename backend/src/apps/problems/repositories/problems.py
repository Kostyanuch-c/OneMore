from django.db.models import Prefetch, Q, QuerySet

from apps.problems.dto import ProblemCreateDTO
from apps.problems.entities import ProblemCreatedEntity, ProblemEntity
from apps.problems.models import Problem, Solution
from apps.problems.repositories.converters import ProblemConverter


class ProblemsRepository:
    model = Problem
    solution_model = Solution
    converter = ProblemConverter

    def get_problem_detail_queryset(self) -> QuerySet[Problem]:
        return self.model.objects.select_related(
            'author',
            'topic__section',
            'topic__section__subject',
        ).prefetch_related(
            'tags',
            Prefetch(
                'solutions',
                queryset=(
                    self.solution_model.objects.select_related(
                        'author'
                    ).order_by('-is_main', 'created_at')
                ),
            ),
        )

    def get_problem_detail_by_id(
        self,
        problem_id: int,
        filters: Q | None = None,
    ) -> ProblemEntity | None:
        queryset = self.get_problem_detail_queryset().filter(pk=problem_id)

        if filters is not None:
            queryset = queryset.filter(filters)

        problem = queryset.first()

        if problem is None:
            return None

        return self.converter.to_entity(
            problem,
            with_solutions=True,
        )

    def create_problem(self, dto: ProblemCreateDTO) -> ProblemCreatedEntity:
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
            problem.tags.set(dto.tag_ids)

        return ProblemCreatedEntity(
            id=problem.pk,
            title=problem.title,
        )
