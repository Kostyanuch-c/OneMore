from api.v1.problems.handlers.profile import router as profile_problems_router
from api.v1.problems.handlers.public import router as public_problems_router
from api.v1.problems.handlers.subject import router as subject_problems_router


__all__ = (
    'profile_problems_router',
    'public_problems_router',
    'subject_problems_router',
)
