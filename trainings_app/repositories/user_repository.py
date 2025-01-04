from datetime import datetime
from trainings_app.schemas.users import CreateUser, GetUser, UpdateUserPut, UpdateUserPatch
from typing import Any, Dict


class UserRepository:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def get_user_from_record(record: dict) -> GetUser:
        """Retrieve GetUser model from dict data"""

        if not record:
            raise ValueError("No record found to convert to GetUser")
        return GetUser(
            id=record['id'],
            username=record['username'],
            password_hash=record['password_hash'],
            email=record['email'],
            role=record['role'],
            created_at=record['created_at'],
            last_login=record['last_login']
        )

    @staticmethod
    def user_data_from_user(user: dict) -> tuple:
        """Returns tuple of user params for processing"""

        keys = []
        values = []
        indexes = []
        counter = 0
        for k, v in user.items():
            keys.append(k)
            values.append(v)
            counter += 1
            indexes.append(counter)
        return keys, values, indexes

    async def create_user(self, user: dict) -> GetUser:
        keys, values, indexes = self.user_data_from_user(user)
        query = f"""
                INSERT INTO users ({', '.join(keys)})
                VALUES ({', '.join([f'${i}' for i in indexes])})
                RETURNING *;
            """
        user_record = await self.db.fetchrow(query, *values)
        return self.get_user_from_record(user_record)

    async def get_user_by_id(self, user_id: int) -> GetUser:
        query = """SELECT * FROM users WHERE id = $1 AND deleted_at IS NULL;"""
        user_record = await self.db.fetchrow(query, user_id)
        return self.get_user_from_record(user_record)

    async def get_user_by_username(self, username: str) -> GetUser:
        query = """SELECT * FROM users WHERE username = $1 AND deleted_at IS NULL;"""
        user_record = await self.db.fetchrow(query, username)
        return self.get_user_from_record(user_record)

    async def delete_user(self, user_attr: dict) -> GetUser:
        if not user_attr or len(user_attr) != 1:
            raise ValueError(f"Invalid user_attr")
        attr_key, attr_value = next(iter(user_attr.items()))
        if attr_key in ('id', 'username', 'email'):
            query = f"""
                UPDATE users
                SET deleted_at = $1
                WHERE {attr_key} = $2 AND deleted_at IS NULL
                RETURNING *;
            """
            user_record = await self.db.fetchrow(query, datetime.now(), attr_value)
            if not user_record:
                raise ValueError(f"User not found")
        else:
            raise ValueError(f"Invalid key '{attr_key}'. Allowed keys for delete operation: 'id', 'username', 'email'.")
        return self.get_user_from_record(user_record)

    async def get_deleted_users(self) -> list[GetUser]:
        query = """
            SELECT id, username, password_hash, email, role, created_at, last_login, deleted_at
            FROM users
            WHERE deleted_at IS NOT NULL;
        """
        deleted_users_records = await self.db.fetch(query)
        deleted_users = [GetUser(**record) for record in deleted_users_records]
        return deleted_users

    async def update_user(self, user_id: int, user: dict) -> GetUser:
        keys, values, indexes = self.user_data_from_user(user)
        set_clause = ", ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
        query = f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ${len(indexes) + 1} AND deleted_at IS NULL
            RETURNING *; 
        """
        values.append(user_id)
        user_record = await self.db.fetchrow(query, *values)
        if not user_record:
            raise ValueError(f"User with id={user_id} not found or already deleted.")
        return self.get_user_from_record(user_record)
