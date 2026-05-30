from django.db.models import Q

from apps.problems.entities import SectionEntity
from apps.problems.models import Section
from apps.problems.repositories.converters import SectionConverter


class SectionRepository:
    model = Section
    converter = SectionConverter

    def get_list_by_subject_id(
        self, *, subject_id: int
    ) -> list[SectionEntity]:
        return [
            self.converter.to_entity(model=section)
            for section in self.model.objects.filter(
                subject_id=subject_id,
            ).order_by('name')
        ]

    def get_section_count(self, *, filters: Q | None) -> int:
        return self.model.objects.filter(filters or Q()).count()
