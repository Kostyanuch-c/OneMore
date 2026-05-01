from django.db.models import TextChoices


class Difficulty(TextChoices):
    EASY = 'easy', 'Лёгкая'
    MEDIUM = 'medium', 'Средняя'
    HARD = 'hard', 'Сложная'
