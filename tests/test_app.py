"""Automated tests for the Cloud Resume API."""

import pytest

from app import create_app
from database import repository


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a Flask test client backed by an isolated temporary database."""
    monkeypatch.setattr(repository, "DATABASE_PATH", tmp_path / "test.db")
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_returns_welcome_message(client):
    """The root endpoint returns its welcome JSON."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json == {"message": "Welcome to my Cloud Resume API!"}


def test_about_returns_seeded_profile(client):
    """A new database contains the initial professional profile."""
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json == {
        "name": "Kian Wilson",
        "course": "Computing",
        "career_goal": "Cloud Engineer",
    }


def test_put_about_updates_profile(client):
    """A valid PUT request updates the stored profile."""
    updated_profile = {
        "name": "Kian Wilson",
        "course": "Computing",
        "career_goal": "Junior Cloud Engineer",
    }

    response = client.put("/about", json=updated_profile)

    assert response.status_code == 200
    assert response.json == updated_profile
    assert client.get("/about").json == updated_profile


def test_put_about_rejects_incomplete_profile(client):
    """An update request must provide every required field."""
    response = client.put("/about", json={"name": "Kian Wilson"})

    assert response.status_code == 400
    assert response.json == {
        "error": "Provide non-empty name, course, and career_goal fields."
    }
