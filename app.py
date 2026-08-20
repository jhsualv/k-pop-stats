# app.py
from flask import Flask, session

from auth import auth
from config import FLASK_SECRET_KEY
from db import get_connection
from ingest import ingest_listening
from queries import get_access_token

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

app.register_blueprint(auth)

@app.route("/ingest/listening")
def ingest_listening_route():
    """Ingest listening data for the currently logged-in user."""

    user_id = session.get("user_id")

    if not user_id:
        return "You must be logged in.", 401

    with get_connection() as conn:
        token = get_access_token(user_id, conn)

        ingest_listening(user_id, token, conn)

    return "Listening data ingested successfully."

if __name__ == "__main__":
    app.run(debug=True)