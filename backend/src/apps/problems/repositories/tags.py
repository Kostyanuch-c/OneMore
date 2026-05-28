from apps.problems.entities import TagEntity
from apps.problems.enums import PublicationStatus
from apps.problems.models import Tag
from apps.problems.repositories.converters import TagConverter


class TagRepository:
    model = Tag
    converter = TagConverter

    def get_list_by_subject_id(self, *, subject_id: int) -> list[TagEntity]:
        return [
            self.converter.to_entity(model=tag)
            for tag in self.model.objects.filter(
                problems__topic__section__subject_id=subject_id,
                problems__status=PublicationStatus.PUBLISHED,
            )
            .distinct()
            .order_by('name')
        ]

    def get_existing_tag_ids(self, *, tag_ids: list[int]) -> set[int]:
        return set(
            self.model.objects.filter(id__in=tag_ids).values_list(
                'id', flat=True
            )
        )
