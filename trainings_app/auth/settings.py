from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = Path(BASE_DIR, "certs", "jwt-private.pem")
    public_key_path: Path = Path(BASE_DIR, "certs", "jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


auth_jwt: AuthJWT = AuthJWT()
