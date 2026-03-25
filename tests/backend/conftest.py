from fastapi.testclient import TestClient

from main import app


def pytest_configure(config):
    del config


import pytest


@pytest.fixture
def client():
    return TestClient(app)
