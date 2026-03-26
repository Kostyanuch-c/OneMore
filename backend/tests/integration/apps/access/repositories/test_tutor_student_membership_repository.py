from django.db.models import Q

from apps.access.entities import TutorStudentMembershipEntity


def test_create_membership(
    tutor_student_membership_repository, user_factory, membership_model
):
    tutor = user_factory()
    student = user_factory()

    membership = tutor_student_membership_repository.create(
        student_id=student.id, tutor_id=tutor.id
    )
    db_membership = membership_model.objects.get(id=membership.id)
    # TODO вынести в helper
    assert isinstance(membership, TutorStudentMembershipEntity)
    assert membership.student_id == student.id
    assert membership.tutor_id == tutor.id
    assert membership.is_active is True
    assert membership.id is not None

    assert db_membership.is_active is True
    assert db_membership.student_id == student.id
    assert db_membership.tutor_id == tutor.id
    assert db_membership.created_at is not None
    assert db_membership.updated_at is not None

    assert db_membership.id == membership.id
    assert db_membership.created_at == membership.created_at
    assert db_membership.updated_at == membership.updated_at

    assert membership_model.objects.count() == 1


def test_has_active_membership_true(
    tutor_student_membership_repository, membership
):
    assert (
        tutor_student_membership_repository.has_active_membership(
            Q(student_id=membership.student.id, tutor_id=membership.tutor.id)
        )
        is True
    )


def test_has_active_membership_false_when_inactive(
    tutor_student_membership_repository, tutor_student_membership_factory
):
    membership = tutor_student_membership_factory(is_active=False)

    assert (
        tutor_student_membership_repository.has_active_membership(
            Q(student_id=membership.student.id, tutor_id=membership.tutor.id)
        )
        is False
    )


def test_has_active_membership_false_when_none(
    tutor_student_membership_repository,
):
    assert (
        tutor_student_membership_repository.has_active_membership(
            Q(student_id=999)
        )
        is False
    )
