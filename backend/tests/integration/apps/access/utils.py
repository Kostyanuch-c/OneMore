from django.db.models import Q


def exact_membership_query(membership):
    return Q(
        student_id=membership.student.id,
        tutor_id=membership.tutor.id,
    )


def missing_student_query(_membership):
    return Q(student_id=999999)
