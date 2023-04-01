import json

from fastapi import status
from starlette.testclient import TestClient

LIST_USERS_URL = "/users/"


def test_list_users(client: TestClient):
    response = client.get(LIST_USERS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == "list users"
