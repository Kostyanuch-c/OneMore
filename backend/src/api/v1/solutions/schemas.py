from ninja import Schema

from apps.problems.dto import (
    SolutionCreateDTO,
    SolutionMutationResult,
    SolutionUpdateDTO,
)


class SolutionMutationOutSchema(Schema):
    problem_id: int
    solution_id: int
    detail_url: str

    @staticmethod
    def from_result(
        result: SolutionMutationResult,
    ) -> SolutionMutationOutSchema:
        return SolutionMutationOutSchema(
            problem_id=result.problem_id,
            solution_id=result.solution_id,
            detail_url=result.detail_url,
        )


class SolutionCreateInSchema(Schema, extra='forbid'):
    name: str
    content: str
    is_published: bool

    def to_dto(self, *, author_id: int, problem_id: int) -> SolutionCreateDTO:
        return SolutionCreateDTO(
            problem_id=problem_id,
            name=self.name,
            content=self.content,
            author_id=author_id,
            is_published=self.is_published,
        )


class SolutionUpdateInSchema(Schema, extra='forbid'):
    name: str | None = None
    content: str | None = None
    is_published: bool | None = None

    def to_dto(self) -> SolutionUpdateDTO:
        return SolutionUpdateDTO(
            data=self.model_dump(exclude_unset=True),
        )


class SetMainSolutionInSchema(Schema, extra='forbid'):
    solution_id: int
