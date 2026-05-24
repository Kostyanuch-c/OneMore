from datetime import datetime
from typing import TYPE_CHECKING

from ninja import Schema

from api.v1.mixins import BaseEnumSchema
from api.v1.profile.schemas import UserShortOutSchema
from api.v1.subjects.schemas import (
    DifficultyOutSchema,
    SectionOutSchema,
    SubjectOutSchema,
    TagOutSchema,
    TopicOutSchema,
)
from apps.problems.dto import (
    ProblemCreateDTO,
    ProblemMutationResult,
    ProblemUpdateDTO,
)
from apps.problems.entities import ProblemEntity, SolutionEntity
from apps.problems.enums import Difficulty, PublicationStatus
from apps.problems.permissions import (
    build_problem_permissions,
    build_solution_permissions,
)


if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser

    from apps.users.models import User


class ProblemCreateInSchema(Schema, extra='forbid'):
    title: str
    question: str
    difficulty: Difficulty
    source: str
    topic_id: int
    tag_ids: list[int]
    status: PublicationStatus = PublicationStatus.DRAFT

    def to_dto(self, *, author_id: int) -> ProblemCreateDTO:
        return ProblemCreateDTO(
            title=self.title,
            question=self.question,
            difficulty=self.difficulty,
            source=self.source,
            topic_id=self.topic_id,
            tag_ids=self.tag_ids,
            author_id=author_id,
            status=self.status,
        )


class ProblemUpdateInSchema(Schema, extra='forbid'):
    title: str | None = None
    question: str | None = None
    difficulty: Difficulty | None = None
    source: str | None = None
    topic_id: int | None = None
    tag_ids: list[int] | None = None
    status: PublicationStatus | None = None

    def to_dto(self) -> ProblemUpdateDTO:
        data = self.model_dump(exclude_unset=True)

        if data.get('difficulty') is not None:
            data['difficulty'] = data['difficulty'].value

        if data.get('status') is not None:
            data['status'] = data['status'].value

        return ProblemUpdateDTO(data=data)


class SolutionOutSchema(Schema, extra='forbid'):
    id: int
    name: str
    content: str
    is_main: bool
    author: UserShortOutSchema | None
    is_published: bool
    permissions: SolutionPermissionsOutSchema

    @staticmethod
    def from_entity(
        entity: SolutionEntity, user: User | AnonymousUser
    ) -> SolutionOutSchema:
        return SolutionOutSchema(
            id=entity.id,
            name=entity.name,
            content=entity.content,
            is_main=entity.is_main,
            author=UserShortOutSchema.from_entity(entity.author)
            if entity.author
            else None,
            is_published=entity.is_published,
            permissions=SolutionPermissionsOutSchema(
                **build_solution_permissions(solution=entity, user=user)
            ),
        )


class ProblemMutationOutSchema(Schema):
    id: int
    subject_slug: str
    detail_url: str

    @staticmethod
    def from_result(
        result: ProblemMutationResult,
    ) -> ProblemMutationOutSchema:
        return ProblemMutationOutSchema(
            id=result.id,
            subject_slug=result.subject_slug,
            detail_url=result.detail_url,
        )


class StatusOutSchema(BaseEnumSchema): ...


class ProblemOutSchema(Schema, extra='forbid'):
    id: int
    title: str
    question: str
    source: str
    difficulty: DifficultyOutSchema
    status: StatusOutSchema
    subject: SubjectOutSchema | None = None
    section: SectionOutSchema
    topic: TopicOutSchema
    tags: list[TagOutSchema]
    author: UserShortOutSchema | None = None
    solutions: list[SolutionOutSchema]
    permissions: ProblemPermissionsOutSchema
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(
        entity: ProblemEntity, user: User | AnonymousUser
    ) -> ProblemOutSchema:
        return ProblemOutSchema(
            id=entity.id,
            title=entity.title,
            question=entity.question,
            source=entity.source,
            difficulty=DifficultyOutSchema.from_option(entity.difficulty),
            status=StatusOutSchema.from_option(entity.status),
            subject=SubjectOutSchema.from_entity(entity.subject)
            if entity.subject
            else None,
            section=SectionOutSchema.from_entity(entity.section),
            topic=TopicOutSchema.from_entity(entity.topic),
            tags=[TagOutSchema.from_entity(tag) for tag in entity.tags],
            author=UserShortOutSchema.from_entity(entity.author)
            if entity.author
            else None,
            solutions=[  # If not a solution is empty list
                SolutionOutSchema.from_entity(entity=solution, user=user)
                for solution in entity.solutions
            ],
            permissions=ProblemPermissionsOutSchema(
                **build_problem_permissions(problem=entity, user=user)
            ),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ProblemPermissionsOutSchema(Schema, extra='forbid'):
    can_edit: bool
    can_create_solution: bool


class SolutionPermissionsOutSchema(Schema, extra='forbid'):
    can_edit: bool
