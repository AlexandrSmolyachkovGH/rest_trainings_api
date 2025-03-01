from pydantic import BaseModel, Field


class TelegramAuth(BaseModel):
    user_id: int = Field(
        description="User ID",
        example=1140,
    )
    code: str = Field(
        description="Authorization code from Telegram",
        example="929113",
    )


class TelegramAuthVerification(BaseModel):
    user_id: int = Field(
        description="User ID",
        example=1140,
    )
    code: str = Field(
        description="Authorization code from Telegram",
        example="929113"
    )
    verified: bool = Field(
        default=False,
        description="Verification status",
        example=True,
    )
