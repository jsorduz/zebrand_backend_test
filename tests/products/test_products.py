import json

from fastapi import status
from starlette.testclient import TestClient

PRODUCTS_URL = "/products/"


def test_list_products(client: TestClient):
    response = client.get(PRODUCTS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == "list products"


def test_create_product(client: TestClient):
    response = client.post(PRODUCTS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["message"] == "create product"


def test_retrieve_product(client: TestClient):
    product_id = 1
    response = client.get(PRODUCTS_URL + f"{product_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == f"retrieve product {product_id}"


def test_patch_product(client: TestClient):
    product_id = 1
    response = client.patch(PRODUCTS_URL + f"{product_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["message"] == f"patch product {product_id}"


def test_delete_product(client: TestClient):
    product_id = 1
    response = client.delete(PRODUCTS_URL + f"{product_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
