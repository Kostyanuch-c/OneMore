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
    response: Any, expected_status: int = HTTPStatus.OK
) -> None:
    assert response.status_code == expected_status

    body = response.json()

    assert set(body.keys()) == API_RESPONSE_KEYS
    assert body['errors'] == []
    assert isinstance(body['meta'], dict)


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
    data = response.json()['data']

    assert isinstance(data, dict)

    return schema.model_validate(data)


def get_api_paginated_items[T: Schema](
    response: Any, schema: type[T]
) -> list[T]:
    data = response.json()['data']

    assert isinstance(data, dict)
    assert set(data.keys()) == API_LIST_PAGINATION_RESPONSE_KEYS
    items, pagination = data['items'], data['pagination']
    assert isinstance(items, list)
    assert isinstance(pagination, dict)
    assert set(pagination.keys()) == API_PAGINATION_RESPONSE_KEYS

    return [schema.model_validate(item) for item in items]


def get_api_errors(response: Any) -> list[dict[str, Any]]:
    errors = response.json()['errors']

    assert isinstance(errors, list)
    error = errors[0]
    assert isinstance(error, dict)
    assert set(error.keys()) == API_ERROR_KEYS

    return errors
