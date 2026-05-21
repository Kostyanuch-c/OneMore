from api.v1.mixins import CreatedAtRangeFilterMixin
from apps.problems.enums import Difficulty


class ProblemsFilterInSchema(CreatedAtRangeFilterMixin, extra='forbid'):
    search: str | None = None

    section_ids: tuple[int, ...] = ()
    topic_ids: tuple[int, ...] = ()
    tag_ids: tuple[int, ...] = ()

    difficulty: Difficulty | None = None
