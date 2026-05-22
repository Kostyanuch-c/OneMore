from apps.problems.entities import TopicEntity
from apps.problems.models import Topic
from apps.problems.repositories.converters import TopicConverter


class TopicRepository:
    model = Topic
    converter = TopicConverter

    def get_list_by_section_ids(
        self, *, section_ids: list[int]
    ) -> list[TopicEntity]:
        return [
            self.converter.to_entity(model=topic)
            for topic in self.model.objects.filter(
                section_id__in=section_ids,
            ).order_by('name')
        ]

    def exists_topic_for_subject(
        self, *, subject_slug: str, topic_id: int
    ) -> bool:
        return self.model.objects.filter(
            pk=topic_id,
            section__subject__slug=subject_slug,
        ).exists()
