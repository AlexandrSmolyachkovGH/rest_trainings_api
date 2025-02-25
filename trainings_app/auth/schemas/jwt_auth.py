from typing import Optional
from pydantic import BaseModel


class AuthToken(BaseModel):
    message: str
    auth_token: str
    telegram_link: Optional[str] = None
    router_path: Optional[str] = None


class RefreshToken(BaseModel):
    message: str
    refresh_token: str
    token_type: str


class AccessToken(BaseModel):
    message: str
    access_token: str
    token_type: str
