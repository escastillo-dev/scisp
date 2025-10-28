# security.py
import jwt, uuid
from datetime import datetime, timedelta
import os

JWT_SECRET   = os.getenv("JWT_SECRET", "dev_secret_change_me")
JWT_ALG      = os.getenv("JWT_ALG", "HS256")
JWT_MINUTES  = int(os.getenv("JWT_MINUTES", "60"))
REFRESH_DAYS = int(os.getenv("REFRESH_DAYS", "30"))

def new_session_id() -> str:
    return str(uuid.uuid4())

def create_access_token(subject: dict) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject, "iat": now, "nbf": now,
        "exp": now + timedelta(minutes=JWT_MINUTES),
        "typ": "access"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def create_refresh_token(subject: dict) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject, "iat": now, "nbf": now,
        "exp": now + timedelta(days=REFRESH_DAYS),
        "typ": "refresh"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
