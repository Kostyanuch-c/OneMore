from apps.problems.entities import SubjectEntity
from apps.problems.models import Subject
from apps.problems.repositories.converters import SubjectConverter


class SubjectRepository:
    model = Subject
    converter = SubjectConverter

    def find_subject_by_slug(self, *, slug: str) -> SubjectEntity | None:
        subject = self.model.objects.filter(slug=slug).first()

        if subject is None:
            return None

        return self.converter.to_entity(model=subject)

    def get_list_subjects(self) -> list[SubjectEntity]:
        return [
            self.converter.to_entity(model=subject)
            for subject in self.model.objects.order_by('name')
        ]
