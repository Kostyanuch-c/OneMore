from ninja import Schema

from apps.problems.dto import DifficultyDTO, ProblemFiltersResult
from apps.problems.entities import (
    SectionEntity,
    TagEntity,
    TopicEntity,
)


class SectionOutSchema(Schema, extra='forbid'):
    id: int
    name: str
    subject_id: int

    @staticmethod
    def from_entity(entity: SectionEntity) -> SectionOutSchema:
        return SectionOutSchema(
            id=entity.id,
            name=entity.name,
            subject_id=entity.subject_id,
        )


class TopicOutSchema(Schema, extra='forbid'):
    id: int
    name: str
    section_id: int

    @staticmethod
    def from_entity(entity: TopicEntity) -> TopicOutSchema:
        return TopicOutSchema(
            id=entity.id,
            name=entity.name,
            section_id=entity.section_id,
        )


class TagOutSchema(Schema, extra='forbid'):
    id: int
    name: str

    @staticmethod
    def from_entity(entity: TagEntity) -> TagOutSchema:
        return TagOutSchema(
            id=entity.id,
            name=entity.name,
        )


class DifficultyOutSchema(Schema, extra='forbid'):
    value: str
    label: str

    @staticmethod
    def from_option(option: DifficultyDTO) -> DifficultyOutSchema:
        return DifficultyOutSchema(
            value=option.value,
            label=option.label,
        )


class ProblemFiltersOutSchema(Schema, extra='forbid'):
    sections: list[SectionOutSchema]
    topics: list[TopicOutSchema]
    tags: list[TagOutSchema]
    difficulties: list[DifficultyOutSchema]

    @staticmethod
    def from_result(result: ProblemFiltersResult) -> ProblemFiltersOutSchema:
        return ProblemFiltersOutSchema(
            sections=[
                SectionOutSchema.from_entity(section)
                for section in result.sections
            ],
            topics=[
                TopicOutSchema.from_entity(topic) for topic in result.topics
            ],
            tags=[TagOutSchema.from_entity(tag) for tag in result.tags],
            difficulties=[
                DifficultyOutSchema.from_option(difficulty)
                for difficulty in result.difficulties
            ],
        )
