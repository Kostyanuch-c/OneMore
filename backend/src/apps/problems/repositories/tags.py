from apps.problems.entities import TagEntity
from apps.problems.models import Tag
from apps.problems.repositories.converters import TagConverter


class TagRepository:
    model = Tag
    converter = TagConverter

    def get_list_by_subject_slug(self, subject_slug: str) -> list[TagEntity]:
        tags = (
            self.model.objects.filter(
                problems__topic__section__subject__slug=subject_slug,
                problems__is_published=True,
            )
            .distinct()
            .order_by('name')
        )

        return [self.converter.to_entity(tag) for tag in tags]
