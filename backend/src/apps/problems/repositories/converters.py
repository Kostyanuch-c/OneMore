from typing import TYPE_CHECKING

from apps.problems.entities import (
    ProblemEntity,
    SectionEntity,
    SolutionEntity,
    SubjectEntity,
    TagEntity,
    TopicEntity,
)
from apps.problems.enums import DifficultyData, PublicationStatusData
from apps.users.repositories.converter import UserConverter


if TYPE_CHECKING:
    from apps.problems.models import (
        Problem,
        Section,
        Solution,
        Subject,
        Tag,
        Topic,
    )


class SubjectConverter:
    @staticmethod
    def to_entity(*, model: Subject) -> SubjectEntity:
        return SubjectEntity(
            id=model.pk,
            name=model.name,
            slug=model.slug,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SectionConverter:
    @staticmethod
    def to_entity(*, model: Section) -> SectionEntity:
        return SectionEntity(
            id=model.pk,
            name=model.name,
            subject_id=model.subject_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class TopicConverter:
    @staticmethod
    def to_entity(*, model: Topic) -> TopicEntity:
        return TopicEntity(
            id=model.pk,
            name=model.name,
            section_id=model.section_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class TagConverter:
    @staticmethod
    def to_entity(*, model: Tag) -> TagEntity:
        return TagEntity(
            id=model.pk,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SolutionConverter:
    @staticmethod
    def to_entity(*, model: Solution) -> SolutionEntity:
        return SolutionEntity(
            id=model.pk,
            problem_id=model.problem_id,
            name=model.name,
            content=model.content,
            author=UserConverter.to_entity(model=model.author)
            if model.author
            else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_main=model.is_main,
            is_published=model.is_published,
        )


class ProblemConverter:
    @staticmethod
    def to_entity(
        *, model: Problem, with_solutions: bool = False
    ) -> ProblemEntity:
        return ProblemEntity(
            id=model.pk,
            title=model.title,
            question=model.question,
            difficulty=DifficultyData(
                value=model.difficulty,
                label=model.get_difficulty_display(),
            ),
            source=model.source,
            topic=TopicConverter.to_entity(model=model.topic),
            tags=[
                TagConverter.to_entity(model=tag) for tag in model.tags.all()
            ],
            author=UserConverter.to_entity(model=model.author)
            if model.author
            else None,
            solutions=[
                SolutionConverter.to_entity(model=solution)
                for solution in model.solutions.all()
            ]
            if with_solutions
            else [],
            status=PublicationStatusData(
                value=model.status,
                label=model.get_status_display(),
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
            section=SectionConverter.to_entity(model=model.topic.section),
        )
