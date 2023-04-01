import json
from uuid import uuid4

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.models import User
from tests.factories import create_user

LOGIN_URL = "/token/"


@pytest.mark.asyncio
async def test_login(client: TestClient):
    await create_user(email="email1@example.com", password="s3cret")
    response = client.post(
        LOGIN_URL, data={"username": "email1@example.com", "password": "s3cret"}
    )
    response_json = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_json
    assert "token_type" in response_json
