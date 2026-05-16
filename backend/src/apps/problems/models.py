from django.conf import settings
from django.db import models
from django.db.models.functions import Lower, Trim

from apps.common.models import BaseTimedModel
from apps.problems.enums import Difficulty
from apps.problems.queryset import ProblemQuerySet


class Subject(BaseTimedModel):
    name = models.CharField(
        verbose_name='Предмет',
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Slug предмета',
        unique=True,
        max_length=50,
        help_text='Например: chemistry, math, physics',
    )

    class Meta:
        db_table = 'subjects'
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self) -> str:
        return self.name


class Section(BaseTimedModel):
    name = models.CharField(
        verbose_name='Раздел',
        max_length=50,
        null=False,
        blank=False,
    )

    subject = models.ForeignKey(
        Subject,
        verbose_name='Предмет',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='sections',
    )

    class Meta:
        db_table = 'sections'
        verbose_name = 'раздел'
        verbose_name_plural = 'Разделы'
        constraints = [
            models.UniqueConstraint(
                'subject',
                Lower(Trim('name')),
                name='unique_section_per_subject',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Topic(BaseTimedModel):
    name = models.CharField(
        verbose_name='Тема',
        max_length=50,
    )

    section = models.ForeignKey(
        Section,
        verbose_name='Раздел',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='topics',
    )

    class Meta:
        db_table = 'topics'
        verbose_name = 'тема'
        verbose_name_plural = 'Темы'
        constraints = [
            models.UniqueConstraint(
                'section',
                Lower(Trim('name')),
                name='unique_topic_per_section',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Tag(BaseTimedModel):
    name = models.CharField(
        verbose_name='Тэг',
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = 'tags'
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Problem(BaseTimedModel):
    title = models.CharField(
        verbose_name='Название задачи',
        max_length=150,
        null=False,
        blank=False,
    )
    question = models.TextField(verbose_name='Дано')
    difficulty = models.CharField(
        verbose_name='Сложность',
        choices=Difficulty.choices,
        max_length=max(len(difficulty) for difficulty in Difficulty.values),
        null=False,
        blank=False,
    )
    source = models.CharField(
        verbose_name='Источник',
        max_length=200,
        blank=True,
        default='',
        help_text='Например: ЕГЭ-2024, Сборник Рудзитиса, Олимпиада МГУ и т.п.',
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть задачу.',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
    )
    topic = models.ForeignKey(
        Topic,
        verbose_name='Тема',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    objects = ProblemQuerySet.as_manager()

    class Meta:
        db_table = 'problems'
        ordering = ('-created_at',)
        default_related_name = 'problems'
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

        indexes = [
            models.Index(fields=['is_published', 'topic', '-created_at'])
        ]

    def __str__(self) -> str:
        return f'{self.title[: settings.MAX_STR_LENGTH]}'


class Solution(BaseTimedModel):
    name = models.CharField(
        verbose_name='Название решения',
        max_length=50,
        blank=False,
        default='Основное решение',
    )
    problem = models.ForeignKey(
        Problem,
        verbose_name='Задача',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    is_main = models.BooleanField(
        verbose_name='Основное решение',
        default=False,
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть решение.',
    )
    content = models.TextField(verbose_name='Решение')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор решения',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        db_table = 'solutions'
        verbose_name = 'решение'
        verbose_name_plural = 'Решения'
        ordering = ('-is_main', 'created_at')
        default_related_name = 'solutions'
        constraints = [
            models.UniqueConstraint(
                fields=['problem'],
                condition=models.Q(is_main=True),
                name='unique_main_solution_per_problem',
            ),
        ]

    def __str__(self) -> str:
        return self.name
