import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as cli:
        yield cli
