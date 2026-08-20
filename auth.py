# auth.py
import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import requests
from flask import Blueprint, redirect, session, request, render_template

from crypto import encrypt
from db import get_connection
from queries import upsert_spotify_token, upsert_user

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    """Display the login page."""
    return render_template("login.html")

@auth.route("/authorize")
def authorize():
    """Redirect the user to Spotify's authorization page."""

    state = secrets.token_urlsafe(32)
    session["spotify_state"] = state
    
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": "user-top-read user-library-read user-read-private",
        "state": state
    }
    
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return redirect(auth_url)


@auth.route("/logout")
def logout():
    """Log the user out by clearing the session."""
    session.clear()
    return redirect("/login")

@auth.route("/callback")
def callback():
    """Handle Spotify's OAuth callback and exchange the code for tokens."""

    # Spotify might redirect back with an error instead of an authorization code.
    if request.args.get("error"):
        return f"Spotify authorization failed: {request.args['error']}", 400

    code = request.args.get("code")
    state = request.args.get("state")
    
    # Retrieve and remove the stored state so it cannot be reused.
    expected_state = session.pop("spotify_state", None)

    # Reject callbacks with a missing or invalid state.
    if not state or not expected_state or state != expected_state:
        return "Invalid state", 400
    
    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
        },
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        timeout=10,
    )

    # Log Spotify's error details server-side without exposing them to the user.
    if not token_response.ok:
        logger.error(
            "Spotify token exchange failed: %s",
            token_response.text,
        )
        return "Failed to exchange authorization code for tokens", 400

    token_data = token_response.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")

    if not access_token or not refresh_token or not expires_in:
        logger.error(
            "Spotify token response missing required fields: %s",
            token_data,
        )
        return "Invalid token response from Spotify", 400

    # Convert Spotify's relative expiration time into an absolute UTC timestamp.
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=expires_in
    )

    # Get the Spotify account information for the authenticated user.
    me_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    if not me_response.ok:
        logger.error(
            "Spotify /v1/me failed: %s",
            me_response.text,
        )
        return "Failed to retrieve Spotify user information", 400

    spotify_user = me_response.json()

    spotify_user_id = spotify_user.get("id")
    display_name = spotify_user.get("display_name")
    image_url = (
        spotify_user.get("images", [{}])[0].get("url")
        if spotify_user.get("images")
        else None
    )

    if not spotify_user_id:
        logger.error("Spotify /v1/me response missing user ID: %s", spotify_user)
        return "Invalid user response from Spotify", 400

    # Encrypt and store the refresh token.
    encrypted_refresh_token = encrypt(refresh_token)

    # Upsert the user into the database.
    with get_connection() as conn:
        user_id = upsert_user(spotify_user_id, display_name, image_url, conn)
        upsert_spotify_token(user_id, access_token, encrypted_refresh_token, expires_at, conn)

    # Store the internal user ID in the session.
    session["user_id"] = user_id
    
    return redirect("/")
