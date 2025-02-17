import abc

from asyncpg import Connection

from trainings_app.db.fields.users import UserFields
from trainings_app.utils.password_hashing import verify_password


class BaseRepository(abc.ABC):

    def __init__(self, conn: Connection):
        self.conn = conn


class AuthJWTRepository(BaseRepository):
    fields = UserFields

    async def validate_auth_user(self, username: str, password: str):
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM users
            WHERE username = $1;
        """
        user_record = await self.conn.fetchrow(query, username)
        if not user_record or not verify_password(password, user_record["password_hash"]):
            return None
        return user_record
