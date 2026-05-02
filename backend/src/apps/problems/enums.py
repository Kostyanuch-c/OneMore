from dataclasses import dataclass

from django.db import models


class Difficulty(models.TextChoices):
    EASY = 'easy', 'Лёгкая'
    MEDIUM = 'medium', 'Средняя'
    HARD = 'hard', 'Сложная'


@dataclass(frozen=True)
class DifficultyData:
    value: str
    label: str
