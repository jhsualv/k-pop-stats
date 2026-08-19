# auth.py
import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import requests
from flask import Blueprint, redirect, session, request

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
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

    # TODO: Call Spotify /v1/me.
    # TODO: Upsert the user into the database.
    # TODO: Encrypt and store the refresh token.
    # TODO: Store the internal user ID in the session.
    # TODO: Redirect to the dashboard.
    
    return f"Token expires at: {expires_at}"
