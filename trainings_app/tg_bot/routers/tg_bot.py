import datetime

from fastapi import HTTPException, APIRouter, status

from trainings_app.tg_bot.schemas.tg_bot import TelegramAuth
from trainings_app.tg_bot.temp_storage import tg_auth_data

router = APIRouter(
    prefix='/tg_bot',
    tags=['tg_bot'],
)


@router.post("/verify_code")
async def verify_tg_code(auth_data: TelegramAuth):
    user_id = auth_data.user_id
    code = auth_data.code

    if user_id not in tg_auth_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code not generated or expired",
        )

    stored_data = tg_auth_data.get(user_id)
    if datetime.datetime.now() > stored_data["code_expiry"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code has expired",
        )

    if code != stored_data["code"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid code",
        )

    tg_auth_data[user_id]["verified"] = True
    