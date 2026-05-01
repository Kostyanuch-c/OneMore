from apps.problems.entities import DifficultyEntity
from apps.problems.enums import Difficulty


def get_difficulties() -> list[DifficultyEntity]:
    return [
        DifficultyEntity(value=value, label=label)
        for value, label in Difficulty.choices
    ]
