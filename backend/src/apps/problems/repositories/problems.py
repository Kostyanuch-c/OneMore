from apps.problems.entities import ProblemEntity
from apps.problems.models import Problem
from apps.problems.repositories.converters import ProblemConverter


class ProblemsRepository:
    model = Problem
    converter = ProblemConverter

    def get_problem_by_id(self, problem_id: int) -> ProblemEntity:
        return self.converter.to_entity(
            self.model.objects.select_related('author', 'topic__section')
            .prefetch_related('tags', 'solutions')
            .get(pk=problem_id),
            with_solutions=True,
        )
