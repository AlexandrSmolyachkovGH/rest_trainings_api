from pydantic import BaseModel


class UserAuthScheme(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
