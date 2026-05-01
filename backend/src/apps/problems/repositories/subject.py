from apps.problems.entities import SubjectEntity
from apps.problems.models import Subject
from apps.problems.repositories.converters import SubjectConverter


class SubjectRepository:
    subject_model = Subject
    converter = SubjectConverter

    def get_list_subjects(self) -> list[SubjectEntity]:
        return [
            self.converter.to_entity(subject)
            for subject in self.subject_model.objects.order_by('name')
        ]
