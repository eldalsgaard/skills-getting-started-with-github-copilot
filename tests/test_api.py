import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


def test_initial_get_activities(client: TestClient):
    # Arrange
    # (default activities state is already loaded)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in activities[activity]["participants"]
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_duplicate(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_signup_missing_activity(client: TestClient):
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404


def test_remove_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_missing_participant(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert response.status_code == 404
