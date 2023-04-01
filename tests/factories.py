import json

from starlette.testclient import TestClient

from app.models import User

LOGIN_URL = "/token/"


async def create_user(email: str, password: str):
    # TODO: create a factory method that creates more than one user at the same time with dummy values
    return await User.create(email=email, hashed_password=User.hash_password(password))


async def login_user(client: TestClient) -> str:
    """
    # TODO: Implement this function as a pytest fixture
    """
    email = "admin@example.com"
    password = "s3cret"
    await User.create(email=email, hashed_password=User.hash_password(password))

    response = client.post(
        LOGIN_URL, data={"username": "admin@example.com", "password": "s3cret"}
    )
    response_json = json.loads(response.content)
    return response_json["access_token"]
