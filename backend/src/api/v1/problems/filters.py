from api.v1.mixins import CreatedAtRangeFilterMixin
from apps.problems.enums import Difficulty, PublicationStatus


class BaseProblemsFilterInSchema(CreatedAtRangeFilterMixin):
    search: str | None = None

    section_ids: tuple[int, ...] = ()
    topic_ids: tuple[int, ...] = ()
    tag_ids: tuple[int, ...] = ()

    difficulty: Difficulty | None = None


class PublicProblemsFilterInSchema(BaseProblemsFilterInSchema): ...


class MyProblemsFilterInSchema(BaseProblemsFilterInSchema):
    status: PublicationStatus | None = None
    subject_slug: str | None = None
