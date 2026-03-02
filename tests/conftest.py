import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset the in‑memory `activities` dictionary before and
    after each test so every test runs against the default state.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
