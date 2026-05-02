from dataclasses import dataclass

from django.db.models import TextChoices


class Difficulty(TextChoices):
    EASY = 'easy', 'Лёгкая'
    MEDIUM = 'medium', 'Средняя'
    HARD = 'hard', 'Сложная'


@dataclass(frozen=True)
class DifficultyData:
    value: str
    label: str
