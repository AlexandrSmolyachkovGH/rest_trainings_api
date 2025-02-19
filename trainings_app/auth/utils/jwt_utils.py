from datetime import timedelta, datetime
from typing import Callable, Awaitable, Optional

import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from trainings_app.auth import settings
from trainings_app.db.connection import get_repo
from trainings_app.exceptions.exceptions import TokenError
from trainings_app.repositories.users import UserRepository
from trainings_app.schemas.users import GetUser, RoleEnum


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
    # decoded = jwt.decode(
    #     token,
    #     public_key,
    #     algorithms=[algorithm],
    # )
    # return decoded
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
        raise TokenError(f"""Invalid token:
        token: {token},
        public_key: {public_key},
        algorithms: {algorithm} в листе,
        """)


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
            detail=f"""Invalid token error: {e},
            Your token: {token}
            """,
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
) -> GetUser:
    """Retrieves and returns UserID from the token payload"""
    return await user_repo.get(user_id=int(payload.get('sub')))


def get_current_auth_user_with_role(
        allowed_roles: Optional[list[RoleEnum]] = None,
) -> Callable[..., Awaitable[GetUser]]:
    """Returns a dependency function that returns user and checks user role"""
    async def inner(
            user_record: GetUser = Depends(get_current_auth_user)
    ) -> GetUser:
        if allowed_roles and user_record.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions for access"
            )
        return user_record
    return inner

