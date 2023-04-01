import json

from fastapi import status
from starlette.testclient import TestClient

USERS_URL = "/users/"


def test_list_users(client: TestClient):
    response = client.get(USERS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == "list users"


def test_create_user(client: TestClient):
    response = client.post(USERS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["message"] == "create user"


def test_retrieve_user(client: TestClient):
    user_id = 1
    response = client.get(USERS_URL + f"{user_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == f"retrieve user {user_id}"


def test_patch_user(client: TestClient):
    user_id = 1
    response = client.patch(USERS_URL + f"{user_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == f"patch user {user_id}"


def test_delete_user(client: TestClient):
    user_id = 1
    response = client.delete(USERS_URL + f"{user_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
