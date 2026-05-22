from apps.problems.exceptions import TopicNotFoundError
from apps.problems.repositories import TopicRepository


class TopicService:
    repository = TopicRepository()

    def ensure_topic_belongs_to_subject(
        self, *, subject_slug: str, topic_id: int
    ) -> None:
        if not self.repository.exists_topic_for_subject(
            subject_slug=subject_slug,
            topic_id=topic_id,
        ):
            raise TopicNotFoundError(
                message='Topic not found for this subject',
                extra={
                    'fields': ['topic_id', 'subject_slug'],
                },
            )
