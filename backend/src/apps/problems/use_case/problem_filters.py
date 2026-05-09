from collections.abc import Callable
from dataclasses import dataclass

from django.utils.functional import cached_property

from apps.common import BaseUseCase
from apps.problems.dto import ProblemFiltersResult
from apps.problems.entities import SubjectEntity
from apps.problems.exceptions import SubjectNotFoundError
from apps.problems.providers import get_difficulties
from apps.problems.repositories import (
    SectionRepository,
    SubjectRepository,
    TagRepository,
    TopicRepository,
)


@dataclass
class GetProblemFilters(BaseUseCase[ProblemFiltersResult]):
    section_repository: SectionRepository
    topic_repository: TopicRepository
    tag_repository: TagRepository
    subject_repository: SubjectRepository
    subject_slug: str

    def act(self) -> ProblemFiltersResult:
        sections = self.section_repository.get_list_by_subject_id(
            subject_id=self.subject.id,  # type: ignore[union-attr]
        )

        section_ids = [section.id for section in sections]

        topics = self.topic_repository.get_list_by_section_ids(
            section_ids=section_ids,
        )

        tags = self.tag_repository.get_list_by_subject_id(
            subject_id=self.subject.id,  # type: ignore[union-attr]
        )

        return ProblemFiltersResult(
            sections=sections,
            topics=topics,
            tags=tags,
            difficulties=get_difficulties(),
        )

    @cached_property
    def subject(self) -> SubjectEntity | None:
        return self.subject_repository.find_subject_by_slug(self.subject_slug)

    def get_validators(self) -> list[Callable[[], None]]:
        return [self.validate_subject_exists]

    def validate_subject_exists(self) -> None:
        if self.subject is None:
            raise SubjectNotFoundError
