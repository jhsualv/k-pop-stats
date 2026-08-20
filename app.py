# app.py
from flask import Flask, render_template, session, redirect, request

from auth import auth
from config import FLASK_SECRET_KEY
from db import get_connection
from ingest import ingest_listening
from queries import get_access_token, get_user
from analysis import get_user_analysis

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

app.register_blueprint(auth)

@app.route("/")
def home():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    time_range = request.args.get("time_range", "short_term")
    selected_group = request.args.get("group", type=int)

    if time_range not in ("short_term", "medium_term", "long_term"):
        time_range = "short_term"

    with get_connection() as conn:
        analysis = get_user_analysis(user_id, conn)
        profile = get_user(user_id, conn)

    return render_template(
        "index.html",
        analysis=analysis,
        profile=profile,
        time_range=time_range,
        selected_group=selected_group,
    )

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