from fastapi import HTTPException, status
from typing import Union
from datetime import datetime

from trainings_app.schemas.users import CreateUser, GetUser
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.user import ConvertUserRecordError, UserAttrError


class UserRepository(BaseRepository):

    @staticmethod
    def get_user_from_record(record: dict) -> GetUser:
        """Retrieve GetUser model from dict data"""

        if not record:
            raise ConvertUserRecordError("No record found to convert to GetUser")
        return GetUser(**record)

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

    @staticmethod
    def check_user_attr(user_attr: dict):
        """Check for the passed attribute"""

        if not user_attr or len(user_attr) != 1 or not isinstance(user_attr, dict):
            raise UserAttrError(f"The passed attr must be a dict with a length of exactly 1.")
        attr_key, attr_value = next(iter(user_attr.items()))
        if attr_key not in ('id', 'username', 'email'):
            raise UserAttrError(
                f"The key of passed attr must belong to one of the following: 'id', 'username', or 'email'."
            )
        return attr_key, attr_value

    async def fetchrow_or_404(self, query: str, *args) -> dict:
        """Check for data retrieval. If no data is found, raise a 404 error."""
        record = await self.db.fetchrow(query, *args)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found."
            )
        return record

    async def create(self, user: CreateUser) -> GetUser:
        keys, values, indexes = self.user_data_from_user(user)
        query = f"""
                INSERT INTO users ({', '.join(keys)})
                VALUES ({', '.join([f'${i}' for i in indexes])})
                RETURNING *;
            """
        user_record = await self.db.fetchrow(query, *values)
        return self.get_user_from_record(user_record)

    async def get(self, user_attr: dict) -> GetUser:
        attr_key, attr_value = self.check_user_attr(user_attr)
        query = f"""SELECT * FROM users WHERE {attr_key} = $1 AND deleted_at IS NULL;"""
        user_record = await self.fetchrow_or_404(query, attr_value)
        return self.get_user_from_record(user_record)

    async def delete(self, user_attr: dict) -> GetUser:
        attr_key, attr_value = self.check_user_attr(user_attr)
        query = f"""
            UPDATE users
            SET deleted_at = $1
            WHERE {attr_key} = $2 AND deleted_at IS NULL
            RETURNING *;
        """
        user_record = await self.fetchrow_or_404(query, datetime.now(), attr_value)
        return self.get_user_from_record(user_record)

    # async def get_active_users(self) -> Union[list[GetUser], list]:
    #
    #     query = """
    #         SELECT id, username, password_hash, email, role, created_at, last_login, deleted_at
    #         FROM users
    #         WHERE deleted_at IS NULL;
    #     """
    #     active_users_records = await self.db.fetch(query)
    #     active_users = [GetUser(**record) for record in active_users_records]
    #     return active_users

    async def get_users(self, user_status: str | None = None) -> Union[list[GetUser], list]:
        status_dct = {'active': 'IS NULL', 'deleted': 'IS NOT NULL'}
        if user_status:
            query = f"""
                SELECT id, username, password_hash, email, role, created_at, last_login, deleted_at
                FROM users
                WHERE deleted_at {status_dct[user_status]};
            """
        else:
            query = f"""
                SELECT id, username, password_hash, email, role, created_at, last_login, deleted_at
                FROM users;
            """
        user_records = await self.db.fetch(query)
        users = [GetUser(**record) for record in user_records]
        return users

    # async def get_deleted_users(self) -> Union[list[GetUser], list]:
    #     query = """
    #         SELECT id, username, password_hash, email, role, created_at, last_login, deleted_at
    #         FROM users
    #         WHERE deleted_at IS NOT NULL;
    #     """
    #     deleted_users_records = await self.db.fetch(query)
    #     deleted_users = [GetUser(**record) for record in deleted_users_records]
    #     return deleted_users

    async def update(self, user_id: int, user: dict) -> GetUser:
        keys, values, indexes = self.user_data_from_user(user)
        set_clause = ", ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
        query = f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ${len(indexes) + 1} AND deleted_at IS NULL
            RETURNING *; 
        """
        values.append(user_id)
        user_record = await self.fetchrow_or_404(query, *values)
        return self.get_user_from_record(user_record)
