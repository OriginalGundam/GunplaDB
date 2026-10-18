
# app.py

# Starts the website

from flask import Flask, render_template
from database import get_connection
from search_routes import search_routes

app = Flask(__name__)

app.register_blueprint(search_routes)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {
        "message": "Welcome to GunplaDB!",
        "status": "Backend is running."
    }


@app.route("/db-health")
def db_health():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()

        return {
            "status": "Database connection successful."
        }

    except Exception:
        app.logger.exception("Database health check failed.")
        return {
            "status": "Database connection failed."
        }, 503

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
