from datetime import timedelta, datetime
import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from trainings_app.auth import settings
from trainings_app.exceptions.exceptions import TokenError


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    """Custom function for the JWT encoding."""
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """Custom function for the JWT decoding."""
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise TokenError("Token has expired")
    except jwt.InvalidTokenError:
        raise TokenError("Invalid token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt-auth/login/")


async def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> dict:
    """Receives new token for the User entity."""
    try:
        payload = decode_jwt(token=token)
    except TokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token: {e}',
        )
    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
) -> int:
    """Retrieves and returns UserID from the token payload"""
    return payload.get('sub')
