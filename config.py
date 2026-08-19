# config.py
import os

from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

def required_env(name : str) -> str:
    """Return an environment variable or raise if it is missing."""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value

# Database configuration
DATABASE_URL = required_env("DATABASE_URL")

# Encryption configuration
ENCRYPTION_KEY = required_env("TOKEN_ENCRYPTION_KEY")

# Flask configuration
FLASK_SECRET_KEY = required_env("FLASK_SECRET_KEY")

# Spotify OAuth configuration
SPOTIFY_CLIENT_ID = required_env("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = required_env("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = required_env("SPOTIFY_REDIRECT_URI")
