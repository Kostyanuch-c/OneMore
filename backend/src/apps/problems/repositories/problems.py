from django.db.models import Prefetch, Q, QuerySet

from apps.problems.entities import ProblemEntity
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
