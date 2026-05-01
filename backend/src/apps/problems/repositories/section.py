from apps.problems.entities import SectionEntity
from apps.problems.models import Section
from apps.problems.repositories.converters import SectionConverter


class SectionRepository:
    model = Section
    converter = SectionConverter

    def get_list_by_subject_slug(
        self, subject_slug: str
    ) -> list[SectionEntity]:
        return [
            self.converter.to_entity(section)
            for section in self.model.objects.filter(
                subject__slug=subject_slug,
            ).order_by('name')
        ]
