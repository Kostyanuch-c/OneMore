from apps.common.base_query_builder import BaseQueryBuilder
from apps.problems.dto import ProfileProblemFilters, PublicProblemFilters


class ProblemQueryBuilder(
    BaseQueryBuilder[ProfileProblemFilters | PublicProblemFilters]
):
    FILTER_LOOKUPS = {
        'subject_slug': 'topic__section__subject__slug',
        'section_ids': 'topic__section_id__in',
        'topic_ids': 'topic_id__in',
        'tag_ids': 'tags__id__in',
        'difficulty': 'difficulty',
        'status': 'status',
        'created_from': 'created_at__gte',
        'created_to': 'created_at__lte',
    }

    SEARCH_FIELDS = (
        'title',
        'question',
        'source',
    )
