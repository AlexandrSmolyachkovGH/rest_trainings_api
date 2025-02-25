import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from trainings_app.db.connection import get_repo
from trainings_app.auth.repositories.jwt_auth import AuthJWTRepository
from trainings_app.auth.schemas.jwt_auth import AuthToken, RefreshToken, AccessToken
from trainings_app.auth.utils.jwt_utils import encode_jwt, decode_jwt
from trainings_app.db_redis.settings import redis_client

router = APIRouter(prefix='/jwt-auth', tags=['JWT-AUTH'])


# @router.post(
#     path='/login/',
#     response_model=TokenInfo,
#     description="Get JWT token for authentication",
#     status_code=status.HTTP_200_OK,
# )
# async def auth_user_issue_jwt(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         auth_repo: AuthJWTRepository = Depends(get_repo(AuthJWTRepository)),
# ) -> TokenInfo:
#     user_record = await auth_repo.validate_auth_user(
#         username=form_data.username,
#         password=form_data.password,
#     )
#     if not user_record:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="The user was not authorized.",
#         )
#     jwt_payload = {
#         "sub": str(user_record["id"]),
#         "username": user_record["username"],
#         "email": user_record["email"],
#         "role": user_record["role"],
#         "exp": 30,
#     }
#     token = encode_jwt(payload=jwt_payload)
#     token_info = TokenInfo(
#         access_token=token,
#         token_type='Bearer'
#     )
#     return token_info

@router.post(
    path='/login/',
    response_model=AuthToken,
    description="Get JWT token for authentication",
    status_code=status.HTTP_200_OK,
)
async def auth_user_by_jwt(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_repo: AuthJWTRepository = Depends(get_repo(AuthJWTRepository)),
) -> AuthToken:
    """Login and receive Auth_JWT"""
    user_record = await auth_repo.validate_auth_user(
        username=form_data.username,
        password=form_data.password,
    )
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user was not authorized.",
        )
    jwt_payload = {
        "sub": str(user_record["id"]),
        "verified": False,
        "username": user_record["username"],
        "email": user_record["email"],
        "role": user_record["role"],
        "exp": 30,
    }
    auth_token = encode_jwt(payload=jwt_payload)
    short_id = str(uuid.uuid4())[:8]
    await redis_client.set(short_id, auth_token, ex=300)
    tg_link = "https://t.me/my_fastapi_training_app_bot"
    tg_query = f"?start={short_id}"
    token_info = AuthToken(
        message="Follow the telegram link for verification.",
        auth_token=auth_token,
        telegram_link=tg_link + tg_query,
    )
    return token_info


@router.post(
    path='/verification/',
    response_model=RefreshToken,
    description="Pass the access verification. Receive a refresh token token.",
    status_code=status.HTTP_200_OK,
)
async def auth_verification(code: str):
    redis_token = await redis_client.get(code)
    if not redis_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid or expired code. Please try again."
        )
    redis_token = decode_jwt(redis_token)
    redis_token["verified"] = True
    refresh_token = encode_jwt(redis_token, expire_timedelta=timedelta(days=365))
    refresh_info = RefreshToken(
        message=f"Successful verification. You have received a refresh token."
        f" Use it to get an access token. You should also save it to refresh the access token in the future.",
        refresh_token=refresh_token,
        token_type="Bearer",
    )
    return refresh_info


@router.post(
    path='/get-access-token/',
    response_model=AccessToken,
    description="Get access_token",
    status_code=status.HTTP_200_OK,
)
async def auth_user_issue_jwt(refresh_token: str):
    decoded = decode_jwt(refresh_token)
    if not decoded or not decoded.get("verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Some issues with refresh token. Please try one more or pass verification again."
        )
    access_token = encode_jwt(decoded, expire_timedelta=timedelta(minutes=60))
    return AccessToken(
        message=f"You have received an access token. Use it to access the application.",
        access_token=access_token,
        token_type="Bearer",
    )
