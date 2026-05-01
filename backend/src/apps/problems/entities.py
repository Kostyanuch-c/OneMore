from dataclasses import dataclass

from apps.common import BaseEntity


@dataclass(frozen=True)
class SubjectEntity(BaseEntity):
    name: str
    slug: str


@dataclass(frozen=True)
class SectionEntity(BaseEntity):
    name: str
    subject_id: int


@dataclass(frozen=True)
class TopicEntity(BaseEntity):
    name: str
    section_id: int


@dataclass(frozen=True)
class TagEntity(BaseEntity):
    name: str


@dataclass(frozen=True)
class DifficultyEntity:
    value: str
    label: str


@dataclass(frozen=True)
class ProblemFiltersEntity:
    sections: list[SectionEntity]
    topics: list[TopicEntity]
    tags: list[TagEntity]
    difficulties: list[DifficultyEntity]
