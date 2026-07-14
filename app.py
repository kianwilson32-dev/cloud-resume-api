"""Entry point for the Cloud Resume API."""

from flask import Flask

from database.repository import get_profile, initialize_database


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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
