from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from trainings_app.db.connection import get_repo
from trainings_app.auth.repositories.jwt_auth import AuthJWTRepository
from trainings_app.auth.schemas.jwt_auth import TokenInfo
from trainings_app.auth.utils.jwt_utils import encode_jwt

router = APIRouter(prefix='/jwt-auth', tags=['JWT-AUTH'])


@router.post(
    path='/login/',
    response_model=TokenInfo,
    description="Create the user",
    status_code=status.HTTP_200_OK,
)
async def auth_user_issue_jwt(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_repo: AuthJWTRepository = Depends(get_repo(AuthJWTRepository)),
) -> TokenInfo:
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
        "username": user_record["username"],
        "email": user_record["email"],
        "role": user_record["role"],
        "exp": 30,
    }
    token = encode_jwt(payload=jwt_payload)
    token_info = TokenInfo(
        access_token=token,
        token_type='Bearer'
    )
    return token_info
