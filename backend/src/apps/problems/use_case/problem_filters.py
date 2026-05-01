from dataclasses import dataclass

from apps.common import BaseUseCase
from apps.problems.entities import ProblemFiltersEntity
from apps.problems.providers import get_difficulties
from apps.problems.repositories import (
    SectionRepository,
    TagRepository,
    TopicRepository,
)


@dataclass
class GetProblemFilters(BaseUseCase[ProblemFiltersEntity]):
    section_repository: SectionRepository
    topic_repository: TopicRepository
    tag_repository: TagRepository
    subject_slug: str

    def act(self) -> ProblemFiltersEntity:
        sections = self.section_repository.get_list_by_subject_slug(
            subject_slug=self.subject_slug,
        )

        section_ids = [section.id for section in sections]

        topics = self.topic_repository.get_list_by_section_ids(
            section_ids=section_ids,
        )

        tags = self.tag_repository.get_list_by_subject_slug(
            subject_slug=self.subject_slug,
        )

        return ProblemFiltersEntity(
            sections=sections,
            topics=topics,
            tags=tags,
            difficulties=get_difficulties(),
        )
