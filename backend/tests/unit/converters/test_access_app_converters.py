from datetime import datetime

from django.utils import timezone

from tests.factories.tutor_student_membership import (
    TutorStudentMembershipFactory,
)
from tests.factories.user import UserFactory

from apps.access.entities import TutorStudentMembershipEntity
from apps.access.repositories.converter import TutorStudentMembershipConverter


def test_tutor_student_membership_converter_to_entity():
    now = timezone.now()

    tutor = UserFactory.build(id=1)
    student = UserFactory.build(id=2)

    model = TutorStudentMembershipFactory.build(
        pk=1,
        tutor=tutor,
        student=student,
        is_active=True,
        created_at=now,
        updated_at=now,
    )

    entity = TutorStudentMembershipConverter.to_entity(model)

    assert isinstance(entity, TutorStudentMembershipEntity)
    assert entity.id == model.pk
    assert entity.tutor_id == model.tutor.id
    assert entity.student_id == model.student.id
    assert entity.is_active == model.is_active
    assert entity.created_at == model.created_at
    assert entity.updated_at == model.updated_at
    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)
