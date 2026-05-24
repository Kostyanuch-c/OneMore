from tests.api.utils import assert_api_paginated_success_response, get_api_data

from api.schemas import ListPaginationResponse
from api.v1.problems.schemas import ProblemOutSchema
from apps.problems.enums import PublicationStatus


def test_anonymous_user_sees_only_published_problems_from_requested_subject(
    client,
    public_problem_list_url,
    subject,
    problems,
    other_subject_problems,
) -> None:
    assert all(
        problem.topic.section.subject_id == subject.id for problem in problems
    )
    assert all(
        problem.topic.section.subject_id != subject.id
        for problem in other_subject_problems
    )

    response = client.get(public_problem_list_url)

    assert_api_paginated_success_response(response=response)

    data = get_api_data(
        response=response,
        schema=ListPaginationResponse[ProblemOutSchema],
    )

    expected_problems = sorted(
        [
            problem
            for problem in problems
            if problem.status == PublicationStatus.PUBLISHED
        ],
        key=lambda problem: problem.created_at,
        reverse=True,
    )

    assert [problem.id for problem in data.items] == [
        problem.id for problem in expected_problems
    ]

    other_subject_problem_ids = {
        problem.id for problem in other_subject_problems
    }

    assert not any(
        problem.id in other_subject_problem_ids for problem in data.items
    )
