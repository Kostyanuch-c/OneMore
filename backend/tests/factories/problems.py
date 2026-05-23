import factory
from factory.django import DjangoModelFactory

from .user import UserFactory
from apps.problems.enums import Difficulty, PublicationStatus
from apps.problems.models import Problem, Section, Solution, Subject, Topic


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Sequence(lambda n: f'Subject {n}')
    slug = factory.Sequence(lambda n: f'subject-{n}')


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    name = factory.Sequence(lambda n: f'Section {n}')
    subject = factory.SubFactory(SubjectFactory)


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Sequence(lambda n: f'Topic {n}')
    section = factory.SubFactory(SectionFactory)


class ProblemFactory(DjangoModelFactory):
    class Meta:
        model = Problem

    title = factory.Sequence(lambda n: f'Problem {n}')
    question = 'What is 2+2?'
    difficulty = Difficulty.EASY
    status = PublicationStatus.PUBLISHED
    topic = factory.SubFactory(TopicFactory)
    author = factory.SubFactory(UserFactory)


class SolutionFactory(DjangoModelFactory):
    class Meta:
        model = Solution

    name = factory.Sequence(lambda n: f'Solution {n}')
    problem = factory.SubFactory(ProblemFactory)
    content = 'It is 4'
    is_main = False
    is_published = True
    author = factory.SubFactory(UserFactory)
