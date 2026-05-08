from datetime import datetime

from ninja import Schema

from api.v1.profile.schemas import UserShortOutSchema
from api.v1.subjects.schemas import (
    DifficultyOutSchema,
    SectionOutSchema,
    TagOutSchema,
    TopicOutSchema,
)
from apps.problems.entities import ProblemEntity, SolutionEntity


# TODO сделать для решения полного автора и подумать про problem id заглушка
class SolutionOutSchema(Schema, extra='forbid'):
    id: int
    name: str
    content: str
    is_main: bool
    author: UserShortOutSchema | None

    @staticmethod
    def from_entity(entity: SolutionEntity) -> SolutionOutSchema:
        return SolutionOutSchema(
            id=entity.id,
            name=entity.name,
            content=entity.content,
            is_main=entity.is_main,
            author=UserShortOutSchema.from_entity(entity.author)
            if entity.author
            else None,
        )


class ProblemOutSchema(Schema, extra='forbid'):
    id: int
    title: str
    question: str
    source: str
    difficulty: DifficultyOutSchema
    section: SectionOutSchema
    topic: TopicOutSchema
    tags: list[TagOutSchema]
    solutions: list[SolutionOutSchema]
    author: UserShortOutSchema | None = None
    is_published: bool
    pub_date: datetime

    @staticmethod
    def from_entity(entity: ProblemEntity) -> ProblemOutSchema:
        return ProblemOutSchema(
            id=entity.id,
            title=entity.title,
            question=entity.question,
            source=entity.source,
            difficulty=DifficultyOutSchema.from_option(entity.difficulty),
            section=SectionOutSchema.from_entity(entity.section),
            topic=TopicOutSchema.from_entity(entity.topic),
            tags=[TagOutSchema.from_entity(tag) for tag in entity.tags],
            solutions=[  # Empty list if no solutions
                SolutionOutSchema.from_entity(solution)
                for solution in entity.solutions
            ],
            author=UserShortOutSchema.from_entity(entity.author)
            if entity.author
            else None,
            is_published=entity.is_published,
            pub_date=entity.pub_date,
        )
