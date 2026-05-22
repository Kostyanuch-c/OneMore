from dataclasses import dataclass

from django.db import models


class Difficulty(models.TextChoices):
    EASY = 'easy', 'Лёгкая'
    MEDIUM = 'medium', 'Средняя'
    HARD = 'hard', 'Сложная'


class PublicationStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    PUBLISHED = 'published', 'Опубликовано'


@dataclass(frozen=True)
class DifficultyData:
    value: str
    label: str


@dataclass(frozen=True)
class PublicationStatusData:
    value: str
    label: str
