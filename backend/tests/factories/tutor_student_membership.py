import factory
from factory.django import DjangoModelFactory

from tests.factories.user import UserFactory

from apps.access.models import TutorStudentMembership


class TutorStudentMembershipFactory(DjangoModelFactory):
    class Meta:
        model = TutorStudentMembership

    tutor = factory.SubFactory(UserFactory)
    student = factory.SubFactory(UserFactory)
    is_active = True
