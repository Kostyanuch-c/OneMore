from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from pytils.translit import slugify

from apps.common.models import BaseTimedModel
from myproject.settings import MAX_STR_LENGTH


User = get_user_model()


class Difficulty(models.TextChoices):
    EASY = 'Easy', 'Easy'
    MEDIUM = 'Medium', 'Medium'
    HARD = 'Hard', 'Hard'


class Subject(BaseTimedModel):
    name = models.CharField(
        verbose_name='Предмет',
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = 'subjects'
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'
        ordering = ('name',)


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
        related_name='topics',
    )

    class Meta:
        db_table = 'sections'
        verbose_name = 'раздел'
        verbose_name_plural = 'Разделы'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['subject', 'name'],
                name='unique_section_per_subject',
            ),
        ]


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
        ordering = ('name',)


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
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['section', 'name'],
                name='unique_topic_per_section',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.section!s} - {self.name}'


class Problem(BaseTimedModel):
    title = models.CharField(
        verbose_name='Название задачи',
        max_length=150,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Адрес для страницы с задачей',
        max_length=50,
        blank=True,
        help_text=(
            'Укажите адрес для страницы с задачей. Используйте только '
            'латиницу, цифры, дефисы и знаки подчёркивания'
        ),
    )
    question = models.TextField(verbose_name='Дано')
    difficulty = models.CharField(
        verbose_name='Сложность',
        choices=Difficulty.choices,
        max_length=20,
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
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время '
        'в будущем — можно делать отложенные публикации.',
        default=timezone.now,
        null=False,
        blank=False,
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
    )
    topic = models.ForeignKey(
        'Topic',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    # TODO решить с автором ставить ли по дефолту машу
    author = models.ForeignKey(
        User,
        verbose_name='Автор задачи',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        db_table = 'problems'
        ordering = ('-pub_date',)
        default_related_name = 'problems'
        verbose_name = 'химическая задача'
        verbose_name_plural = 'Химические задачи'

        indexes = [
            models.Index(fields=['is_published']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['-pub_date']),
            models.Index(fields=['is_published', 'topic', '-pub_date']),
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title[:MAX_STR_LENGTH]} | {self.slug}'


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
    content = models.TextField(verbose_name='Решение')
    author = models.ForeignKey(
        User,
        verbose_name='Автор решения',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        db_table = 'solutions'
        verbose_name = 'решение'
        verbose_name_plural = 'Решения'
        ordering = ('created_at',)
        default_related_name = 'solutions'

    def __str__(self) -> str:
        return f'{self.name} — {self.problem!s}'
