from apps.problems.dto import DifficultyDTO
from apps.problems.enums import Difficulty


def get_difficulties() -> list[DifficultyDTO]:
    return [
        DifficultyDTO(value=value, label=label)
        for value, label in Difficulty.choices
    ]
