from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config.settings import settings  # Ensure your settings path is correct

ALGORITHM = settings.ALGORITHM

def create_token(data: dict, expires_delta: timedelta):
    """Internal helper to encode the JWT with user data and expiry."""
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict):
    """Generates a short-lived access token."""
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expires_delta)

def create_refresh_token(data: dict):
    """Generates a long-lived refresh token."""
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(data, expires_delta)

def verify_token(token: str):
    """
    Verifies the token signature and expiration.
    Returns the decoded payload or raises a JWTError.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Re-raise the error for the caller (usually your Auth middleware)
        raise e
