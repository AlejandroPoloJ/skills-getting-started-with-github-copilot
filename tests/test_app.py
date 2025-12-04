import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Try to sign up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400


def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Programming Class"
    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Removed")
    # Try to remove again (should fail)
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404


def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404


def test_remove_participant_not_found():
    response = client.delete("/activities/Chess Club/participants/notfound@mergington.edu")
    assert response.status_code == 404
