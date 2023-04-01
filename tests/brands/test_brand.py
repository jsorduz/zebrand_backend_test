import json
from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models import Brand
from tests.factories import create_brand, login_user

BRANDS_URL = "/brands/"


@pytest.mark.asyncio
async def test_list_brands(client: TestClient):
    await create_brand(name="Brand1")
    await create_brand(name="Brand2")
    await create_brand(name="Brand3")

    access_token = await login_user(client)
    response = client.get(
        BRANDS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert len(response_json) == 3


@pytest.mark.asyncio
async def test_create_brand(client: TestClient):
    access_token = await login_user(client)
    response = client.post(
        BRANDS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Brand1"},
    )
    response_json = json.loads(response.content)
    brand_id = response_json["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert await Brand.get_or_none(id=brand_id)


@pytest.mark.asyncio
async def test_create_brand_missing_name(client: TestClient):
    access_token = await login_user(client)
    response = client.post(
        BRANDS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        json={},
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"][0]["msg"] == "field required"


@pytest.mark.asyncio
async def test_retrieve_brand(client: TestClient):
    access_token = await login_user(client)
    brand = await create_brand(name="Brand1")
    brand_id = brand.id
    response = client.get(
        BRANDS_URL + f"{brand_id}/", headers={"Authorization": f"Bearer {access_token}"}
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["name"] == "Brand1"


@pytest.mark.asyncio
async def test_patch_brand(client: TestClient):
    access_token = await login_user(client)
    brand = await create_brand(name="Brand1")
    brand_id = brand.id
    response = client.patch(
        BRANDS_URL + f"{brand_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Brand2"},
    )
    response_json = json.loads(response.content)

    brand_in_db = await Brand.get(id=brand_id)
    assert response.status_code == status.HTTP_200_OK
    assert response_json["name"] == "Brand2"
    assert brand_in_db.name == "Brand2"


@pytest.mark.asyncio
async def test_delete_brand(client: TestClient):
    access_token = await login_user(client)
    brand = await create_brand(name="Brand1")
    brand_id = brand.id
    response = client.delete(
        BRANDS_URL + f"{brand_id}/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    assert not await Brand.get_or_none(id=brand_id)


@pytest.mark.asyncio
async def test_not_found_brand(client: TestClient):
    brand_id = uuid4()
    access_token = await login_user(client)

    response = client.get(
        BRANDS_URL + f"{brand_id}/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.patch(
        BRANDS_URL + f"{brand_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Brand2"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.delete(
        BRANDS_URL + f"{brand_id}/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
