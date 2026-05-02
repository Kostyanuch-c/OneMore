from django.db.models import Prefetch

from apps.problems.entities import ProblemEntity
from apps.problems.models import Problem, Solution
from apps.problems.repositories.converters import ProblemConverter


class ProblemsRepository:
    model = Problem
    solution_model = Solution
    converter = ProblemConverter

    def get_problem_by_id(self, problem_id: int) -> ProblemEntity:
        return self.converter.to_entity(
            self.model.objects.select_related(
                'author',
                'topic__section',
            )
            .prefetch_related(
                'tags',
                Prefetch(
                    'solutions',
                    queryset=self.solution_model.objects.select_related(
                        'author'
                    ),
                ),
            )
            .get(pk=problem_id)
        )
