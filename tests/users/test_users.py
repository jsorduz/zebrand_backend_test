import json
from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models import User
from tests.factories import create_user

USERS_URL = "/users/"


@pytest.mark.asyncio
async def test_list_users(client: TestClient):
    await create_user(email="email1@example.com", password="s3cret")
    await create_user(email="email2@example.com", password="s3cret")
    await create_user(email="email3@example.com", password="s3cret")
    response = client.get(USERS_URL)
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert len(response_json) == 3
    for record in response_json:
        assert not "password" in record
        assert not "hashed_password" in record


@pytest.mark.asyncio
async def test_create_user(client: TestClient):
    response = client.post(
        USERS_URL, json={"email": "email1@example.com", "password": "s3cret"}
    )
    response_json = json.loads(response.content)
    user_id = response_json["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert not "password" in response_json
    assert not "hashed_password" in response_json
    assert await User.get_or_none(id=user_id)


@pytest.mark.asyncio
async def test_create_user_missing_password(client: TestClient):
    response = client.post(USERS_URL, json={"email": "email1@example.com"})
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"][0]["msg"] == "field required"


@pytest.mark.asyncio
async def test_retrieve_user(client: TestClient):
    user = await create_user(email="email1@example.com", password="s3cret")
    user_id = user.id
    response = client.get(USERS_URL + f"{user_id}/")
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_json["email"] == "email1@example.com"
    assert not "password" in response_json
    assert not "hashed_password" in response_json


@pytest.mark.asyncio
async def test_patch_user(client: TestClient):
    user = await create_user(email="email1@example.com", password="s3cret")
    user_id = user.id
    response = client.patch(
        USERS_URL + f"{user_id}/", json={"email": "email2@example.com"}
    )
    response_json = json.loads(response.content)

    user_in_db = await User.get(id=user_id)
    assert response.status_code == status.HTTP_200_OK
    assert response_json["email"] == "email2@example.com"
    assert user_in_db.email == "email2@example.com"


@pytest.mark.asyncio
async def test_delete_user(client: TestClient):
    user = await create_user(email="email1@example.com", password="s3cret")
    user_id = user.id
    response = client.delete(USERS_URL + f"{user_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    assert not await User.get_or_none(id=user_id)


@pytest.mark.asyncio
async def test_not_found_user(client: TestClient):
    user_id = uuid4()

    response = client.get(USERS_URL + f"{user_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.patch(
        USERS_URL + f"{user_id}/", json={"email": "email2@example.com"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.delete(USERS_URL + f"{user_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
