from apps.problems.enums import Difficulty, DifficultyData


def get_difficulties() -> list[DifficultyData]:
    return [
        DifficultyData(value=value, label=label)
        for value, label in Difficulty.choices
    ]
