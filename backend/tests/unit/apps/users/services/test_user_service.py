from http import HTTPStatus


def test_fake(auth_client):
    response = auth_client.get('/api/v1/admin/users')

    assert  response.status_code == HTTPStatus.UNAUTHORIZED
