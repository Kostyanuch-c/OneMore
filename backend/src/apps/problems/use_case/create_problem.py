from collections.abc import Callable
from dataclasses import dataclass

from django.db import transaction

from apps.common import BaseUseCase
from apps.problems.dto import ProblemCreateDTO, ProblemCreateResult
from apps.problems.services import ProblemService, TagService, TopicService


@dataclass
class CreateProblemUseCase(BaseUseCase[ProblemCreateResult]):
    problem_service: ProblemService
    topic_service: TopicService
    tag_service: TagService
    create_data: ProblemCreateDTO
    subject_slug: str

    @transaction.atomic()
    def act(self) -> ProblemCreateResult:
        # transaction because we need to create tags in a problem
        created_problem = self.problem_service.create_problem(
            dto=self.create_data,
        )

        return ProblemCreateResult(
            id=created_problem.id,
            title=created_problem.title,
            subject_slug=self.subject_slug,
            detail_url=f'{self.subject_slug}/problems/{created_problem.id}',
        )

    def get_validators(self) -> list[Callable[[], None]]:
        return [
            self.validate_topic_belongs_to_subject,
            self.validate_tags_exist,
        ]

    def validate_topic_belongs_to_subject(self) -> None:
        self.topic_service.ensure_topic_belongs_to_subject(
            topic_id=self.create_data.topic_id,
            subject_slug=self.subject_slug,
        )

    def validate_tags_exist(self) -> None:
        self.tag_service.ensure_tags_exist(
            tag_ids=self.create_data.tag_ids,
        )
