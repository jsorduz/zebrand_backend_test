import json

from fastapi import status
from starlette.testclient import TestClient

LIST_PRODUCTS_URL = "/products/"


def test_list_users(client: TestClient):
    response = client.get(LIST_PRODUCTS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == "list products"
