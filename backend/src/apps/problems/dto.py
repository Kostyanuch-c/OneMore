from dataclasses import dataclass
from datetime import datetime

from apps.problems.entities import (
    SectionEntity,
    TagEntity,
    TopicEntity,
)
from apps.problems.enums import DifficultyData


@dataclass(frozen=True)
class PublicProblemFilters:
    subject_slug: str

    search: str | None = None
    section_ids: tuple[int, ...] = ()
    topic_ids: tuple[int, ...] = ()
    tag_ids: tuple[int, ...] = ()
    difficulty: str | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None


@dataclass(frozen=True)
class ProfileProblemFilters:
    subject_slug: str | None = None
    status: str | None = None

    search: str | None = None
    section_ids: tuple[int, ...] = ()
    topic_ids: tuple[int, ...] = ()
    tag_ids: tuple[int, ...] = ()
    difficulty: str | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None


@dataclass(frozen=True)
class ProblemFiltersResult:
    sections: list[SectionEntity]
    topics: list[TopicEntity]
    tags: list[TagEntity]
    difficulties: list[DifficultyData]


@dataclass(frozen=True)
class ProblemCreateDTO:
    title: str
    question: str
    difficulty: str
    source: str
    topic_id: int
    tag_ids: list[int]
    author_id: int
    status: str


@dataclass(frozen=True)
class ProblemMutationResult:
    id: int
    subject_slug: str
    detail_url: str


@dataclass(frozen=True)
class ProblemUpdateDTO:
    data: dict[str, object]


@dataclass(frozen=True)
class SolutionCreateDTO:
    problem_id: int
    name: str
    content: str
    author_id: int
    is_published: bool


@dataclass(frozen=True)
class SolutionUpdateDTO:
    data: dict[str, object]


@dataclass(frozen=True)
class SolutionMutationResult:
    solution_id: int
    problem_id: int
    detail_url: str
