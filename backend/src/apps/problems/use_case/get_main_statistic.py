from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.problems.dto import MainStatistics
from apps.problems.services import (
    ProblemService,
    SectionService,
    SolutionService,
    TopicService,
)


@dataclass
class GetMainStatistic(BaseUseCase[MainStatistics]):
    problem_service: ProblemService
    solution_service: SolutionService
    section_service: SectionService
    topic_service: TopicService

    def act(self) -> MainStatistics:
        return MainStatistics(
            total_problems=self.problem_service.get_all_published_problem_count(),
            total_solutions=self.solution_service.get_all_published_solution_count(),
            total_topics=self.topic_service.get_all_topic_count(),
            total_sections=self.section_service.get_all_section_count(),
        )
