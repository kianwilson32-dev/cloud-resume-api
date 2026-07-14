"""Entry point for the Cloud Resume API."""

from flask import Flask, request

from database.repository import get_profile, initialize_database, update_profile


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    initialize_database()

    @app.get("/")
    def home() -> dict[str, str]:
        """Return a welcome message for the API."""
        return {"message": "Welcome to my Cloud Resume API!"}

    @app.get("/about")
    def about() -> dict[str, str]:
        """Return the professional profile stored in the database."""
        return get_profile()

    @app.put("/about")
    def update_about() -> tuple[dict[str, str], int] | dict[str, str]:
        """Replace the stored professional profile with validated JSON data."""
        profile = request.get_json(silent=True)
        required_fields = {"name", "course", "career_goal"}

        if not isinstance(profile, dict):
            return {"error": "A JSON request body is required."}, 400

        if set(profile) != required_fields or not all(
            isinstance(profile[field], str) and profile[field].strip()
            for field in required_fields
        ):
            return {
                "error": "Provide non-empty name, course, and career_goal fields."
            }, 400

        return update_profile(profile)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
