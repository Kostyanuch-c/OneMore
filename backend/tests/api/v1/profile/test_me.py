from tests.api.utils import (
    assert_api_success_response,
    get_api_data,
)

from api.v1.profile.schemas import UserOutSchema


def test_get_profile_me_success(
    tutor_client,
    profile_me_get_url: str,
    tutor,
) -> None:
    response = tutor_client.get(profile_me_get_url)

    assert_api_success_response(response=response)
    user_data = get_api_data(response=response, schema=UserOutSchema)

    assert user_data.email == tutor.email
    assert user_data.username == tutor.username
    assert user_data.id == tutor.id
