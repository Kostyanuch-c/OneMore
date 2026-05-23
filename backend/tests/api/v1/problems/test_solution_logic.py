import json
from http import HTTPStatus

from django.urls import reverse

import pytest

from tests.api.utils import (
    assert_api_failure_response,
)
from tests.factories.problems import ProblemFactory, SolutionFactory


@pytest.mark.django_db
def test_cannot_hide_main_solution(tutor_client, tutor):
    problem = ProblemFactory(author=tutor)
    solution = SolutionFactory(
        problem=problem, author=tutor, is_main=True, is_published=True
    )

    url = reverse(
        'api-v1:update_solution',
        kwargs={'problem_id': problem.id, 'solution_id': solution.id},
    )

    response = tutor_client.patch(
        url,
        data=json.dumps({'is_published': False}),
        content_type='application/json',
    )

    assert_api_failure_response(response, HTTPStatus.CONFLICT)
    assert (
        response.json()['errors'][0]['message']
        == 'Main solution cannot be hidden'
    )


@pytest.mark.django_db
def test_cannot_set_hidden_solution_as_main(tutor_client, tutor):
    problem = ProblemFactory(author=tutor)
    solution = SolutionFactory(
        problem=problem, author=tutor, is_main=False, is_published=False
    )

    url = reverse(
        'api-v1:set_main_solution', kwargs={'problem_id': problem.id}
    )

    response = tutor_client.patch(
        url,
        data=json.dumps({'solution_id': solution.id}),
        content_type='application/json',
    )

    assert_api_failure_response(response, HTTPStatus.CONFLICT)
    assert (
        response.json()['errors'][0]['message']
        == 'Hidden solution cannot be main'
    )
