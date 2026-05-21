from apps.common.base_filter_service import BaseQueryBuilder
from apps.problems.dto import ProblemFilters


class ProblemQueryBuilder(BaseQueryBuilder[ProblemFilters]):
    FILTER_LOOKUPS = {
        'section_ids': 'topic__section_id__in',
        'topic_ids': 'topic_id__in',
        'tag_ids': 'tags__id__in',
        'difficulty': 'difficulty',
        'is_published': 'is_published',
        'created_from': 'created_at__gte',
        'created_to': 'created_at__lte',
    }

    SEARCH_FIELDS = (
        'title',
        'question',
        'source',
    )
