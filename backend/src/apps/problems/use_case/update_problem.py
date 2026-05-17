from collections.abc import Callable
from dataclasses import dataclass

from django.db import transaction

from apps.common import BaseUseCase
from apps.problems.dto import (
    ProblemMutationResult,
    ProblemUpdateDTO,
)
from apps.problems.services import ProblemService, TagService, TopicService


@dataclass
class UpdateProblemUseCase(BaseUseCase[ProblemMutationResult]):
    problem_service: ProblemService
    topic_service: TopicService
    tag_service: TagService
    update_data: ProblemUpdateDTO
    problem_id: int
    subject_slug: str

    @transaction.atomic()
    def act(self) -> ProblemMutationResult:
        # transaction because we need to update tags in a problem
        problem_id = self.problem_service.update_problem(
            dto=self.update_data,
            problem_id=self.problem_id,
        )

        return ProblemMutationResult(
            id=problem_id,
            subject_slug=self.subject_slug,
            detail_url=f'{self.subject_slug}/problems/{problem_id}',
        )

    def get_validators(self) -> list[Callable[[], None]]:
        return [
            self.validate_topic_belongs_to_subject,
            self.validate_tags_exist,
        ]

    def validate_topic_belongs_to_subject(self) -> None:
        if (topic_id := self.update_data.data.get('topic_id')) is not None:
            self.topic_service.ensure_topic_belongs_to_subject(
                topic_id=topic_id,  # type: ignore[arg-type]
                subject_slug=self.subject_slug,
            )

    def validate_tags_exist(self) -> None:
        if (tag_ids := self.update_data.data.get('tag_ids')) is not None:
            self.tag_service.ensure_tags_exist(
                tag_ids=tag_ids  # type: ignore[arg-type]
            )
