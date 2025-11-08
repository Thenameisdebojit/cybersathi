# backend/app/services/security.py
from datetime import datetime, timedelta
import jwt
from app.config import Settings
from typing import Optional

settings = Settings()

def create_access_token(subject: dict, expires_minutes: int = 60*24) -> str:
    payload = subject.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire})
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception:
        return None
