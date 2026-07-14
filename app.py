"""Entry point for the Cloud Resume API."""

from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.get("/")
    def home() -> dict[str, str]:
        """Return a welcome message for the API."""
        return {"message": "Welcome to my Cloud Resume API!"}

    @app.get("/about")
    def about() -> dict[str, str]:
        """Return a short professional profile."""
        return {
            "name": "Kian Wilson",
            "course": "Computing",
            "career_goal": "Cloud Engineer",
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
