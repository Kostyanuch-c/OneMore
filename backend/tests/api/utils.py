from http import HTTPStatus
from typing import Any

from ninja import Schema

from api.filters import PaginationOut
from api.schemas import ApiError, ApiResponse, ListPaginationResponse


API_RESPONSE_KEYS = set(ApiResponse.model_fields.keys())
API_ERROR_KEYS = set(ApiError.model_fields.keys())
API_LIST_PAGINATION_RESPONSE_KEYS = set(
    ListPaginationResponse.model_fields.keys()
)
API_PAGINATION_RESPONSE_KEYS = set(PaginationOut.model_fields.keys())


def assert_api_success_response(
    response: Any,
    expected_status: int = HTTPStatus.OK,
) -> None:
    assert response.status_code == expected_status

    body = response.json()

    assert set(body.keys()) == API_RESPONSE_KEYS
    assert body['errors'] == []
    assert isinstance(body['meta'], dict)
    assert isinstance(body['data'], dict)


def assert_api_paginated_success_response(
    response: Any,
    expected_status: int = HTTPStatus.OK,
) -> None:
    assert_api_success_response(response, expected_status)

    data = response.json()['data']

    assert set(data.keys()) == API_LIST_PAGINATION_RESPONSE_KEYS

    items, pagination = data['items'], data['pagination']

    assert isinstance(items, list)
    assert isinstance(pagination, dict)
    assert set(pagination.keys()) == API_PAGINATION_RESPONSE_KEYS


def assert_api_failure_response(response: Any, expected_status: int) -> None:
    assert response.status_code == expected_status

    body = response.json()

    assert set(body.keys()) == API_RESPONSE_KEYS
    assert isinstance(body['meta'], dict)
    assert isinstance(body['errors'], list)
    assert body['errors']

    for error in body['errors']:
        assert set(error.keys()) == API_ERROR_KEYS
        assert isinstance(error['message'], str)
        assert error['message']
        assert error['extra'] is None or isinstance(error['extra'], dict)


def get_api_data[T: Schema](response: Any, schema: type[T]) -> T:
    return schema.model_validate(response.json()['data'])


def get_api_paginated_items[T: Schema](
    response: Any,
    schema: type[T],
) -> list[T]:
    return [
        schema.model_validate(item)
        for item in response.json()['data']['items']
    ]


def get_api_errors(response: Any) -> list[ApiError]:
    return [
        ApiError.model_validate(item) for item in response.json()['errors']
    ]
