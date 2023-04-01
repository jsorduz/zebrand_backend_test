import json
from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models import Product
from tests.factories import create_product, login_user

PRODUCTS_URL = "/products/"


@pytest.mark.asyncio
async def test_list_products(client: TestClient):
    await create_product(sku="Sku1", price=1.0, name="Product1")
    await create_product(sku="Sku2", price=1.0, name="Product2")
    await create_product(sku="Sku3", price=1.0, name="Product3")

    access_token = await login_user(client)
    response = client.get(
        PRODUCTS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert len(response_json) == 3


@pytest.mark.asyncio
async def test_list_products_anomyous_user(client: TestClient):
    await create_product(sku="Sku1", price=1.0, name="Product1")
    await create_product(sku="Sku2", price=1.0, name="Product2")
    await create_product(sku="Sku3", price=1.0, name="Product3")

    response = client.get(PRODUCTS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert len(response_json) == 3


@pytest.mark.asyncio
async def test_create_product(client: TestClient):
    access_token = await login_user(client)
    response = client.post(
        PRODUCTS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"sku": "Sku1", "name": "Product1", "price": 1.0},
    )
    response_json = json.loads(response.content)
    product_id = response_json["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert await Product.get_or_none(id=product_id)


@pytest.mark.asyncio
async def test_create_product_missing_name(client: TestClient):
    access_token = await login_user(client)
    response = client.post(
        PRODUCTS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        json={},
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"][0]["msg"] == "field required"


@pytest.mark.asyncio
async def test_retrieve_product(client: TestClient):
    access_token = await login_user(client)
    product = await create_product(sku="Sku1", price=1.0, name="Product1")
    product_id = product.id
    response = client.get(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["name"] == "Product1"


@pytest.mark.asyncio
async def test_retrieve_product_anonymous_user(client: TestClient):
    product = await create_product(sku="Sku1", price=1.0, name="Product1")
    product_id = product.id
    response = client.get(PRODUCTS_URL + f"{product_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["name"] == "Product1"


@pytest.mark.asyncio
async def test_patch_product(client: TestClient):
    access_token = await login_user(client)
    product = await create_product(sku="Sku1", price=1.0, name="Product1")
    product_id = product.id
    response = client.patch(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Product2"},
    )
    response_json = json.loads(response.content)

    product_in_db = await Product.get(id=product_id)
    assert response.status_code == status.HTTP_200_OK
    assert response_json["name"] == "Product2"
    assert product_in_db.name == "Product2"


@pytest.mark.asyncio
async def test_delete_product(client: TestClient):
    access_token = await login_user(client)
    product = await create_product(sku="Sku1", price=1.0, name="Product1")
    product_id = product.id
    response = client.delete(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    assert not await Product.get_or_none(id=product_id)


@pytest.mark.asyncio
async def test_not_found_product(client: TestClient):
    product_id = uuid4()
    access_token = await login_user(client)

    response = client.get(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.patch(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Product2"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.delete(
        PRODUCTS_URL + f"{product_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
