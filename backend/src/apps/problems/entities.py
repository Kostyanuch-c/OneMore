from dataclasses import dataclass
from datetime import datetime

from apps.common import BaseEntity
from apps.problems.enums import DifficultyData
from apps.users.entities import UserEntity


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
class SolutionEntity(BaseEntity):
    problem_id: int
    name: str
    content: str
    author_id: int | None
    is_main: bool


@dataclass(frozen=True)
class ProblemEntity(BaseEntity):
    title: str
    question: str
    difficulty: DifficultyData
    source: str
    pub_date: datetime
    is_published: bool
    author: UserEntity | None
    section: SectionEntity
    topic: TopicEntity
    tags: list[TagEntity]
    solutions: list[SolutionEntity] | None = None
