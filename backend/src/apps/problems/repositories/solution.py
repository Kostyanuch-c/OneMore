from apps.problems.models import Solution
from apps.problems.repositories.converters import SolutionConverter


class ProblemsRepository:
    model = Solution
    converter = SolutionConverter

    def create_solution(self) -> int:
        return 1
