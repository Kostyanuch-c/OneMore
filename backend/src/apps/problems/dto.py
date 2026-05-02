from dataclasses import dataclass
from datetime import datetime

from apps.problems.entities import (
    ProblemEntity,
    SectionEntity,
    SolutionEntity,
    SubjectEntity,
    TagEntity,
    TopicEntity,
)
from apps.problems.enums import DifficultyData


@dataclass(frozen=True)
class ProblemFiltersResult:
    sections: list[SectionEntity]
    topics: list[TopicEntity]
    tags: list[TagEntity]
    difficulties: list[DifficultyData]


@dataclass(frozen=True)
class ProblemDetailResult:
    problem: ProblemEntity
    subject: SubjectEntity
    section: SectionEntity
    topic: TopicEntity
    tags: list[TagEntity]
    solutions: list[SolutionEntity]


@dataclass(frozen=True)
class ProblemCreateDTO:
    title: str
    question: str
    difficulty: str
    source: str | None
    topic_id: int
    tag_ids: list[int] | None
    author_id: int
    is_published: bool | None
    pub_date: datetime | None


@dataclass(frozen=True)
class ProblemUpdateDTO:
    title: str | None = None
    question: str | None = None
    difficulty: str | None = None
    source: str | None = None
    topic_id: int | None = None
    tag_ids: list[int] | None = None
    is_published: bool | None = None


@dataclass(frozen=True)
class SolutionCreateDTO:
    problem_id: int
    name: str
    content: str
    author_id: int


@dataclass(frozen=True)
class SolutionUpdateDTO:
    name: str | None = None
    content: str | None = None
