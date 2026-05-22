from typing import TYPE_CHECKING, TypedDict

from apps.problems.entities import ProblemEntity, SolutionEntity


if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser

    from apps.users.models import User


class ProblemPermissionsData(TypedDict):
    can_edit: bool
    can_create_solution: bool


class SolutionPermissionsData(TypedDict):
    can_edit: bool


def build_problem_permissions(
    *, problem: ProblemEntity, user: User | AnonymousUser
) -> ProblemPermissionsData:
    if not user.is_authenticated:
        return {
            'can_edit': False,
            'can_create_solution': False,
        }

    is_problem_author = (problem.author and problem.author.id) == user.pk
    is_tutor = user.is_staff or user.is_tutor

    return {
        'can_edit': is_problem_author,
        'can_create_solution': is_tutor,
    }


def build_solution_permissions(
    *, solution: SolutionEntity, user: User | AnonymousUser
) -> SolutionPermissionsData:
    if not user.is_authenticated:
        return {
            'can_edit': False,
        }

    is_solution_author = (solution.author and solution.author.id) == user.pk

    return {
        'can_edit': is_solution_author,
    }
