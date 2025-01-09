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

    async def create(self, user: CreateUser) -> GetUser:
        keys, values, indexes = self.data_from_dict(user)
        query = f"""
                INSERT INTO users ({', '.join(keys)})
                VALUES ({', '.join([f'${i}' for i in indexes])})
                RETURNING *;
            """
        user_record = await self.db.fetchrow(query, *values)
        return self.get_user_from_record(user_record)

    async def get(self, user_attrs: dict) -> GetUser:
        keys, values, indexes = self.data_from_dict(user_attrs)
        allowed_keys = ('id', 'username', 'email')
        if all(key in allowed_keys for key in keys):
            where_clause = " AND ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
            if not where_clause:
                query = "SELECT * FROM users WHERE deleted_at IS NULL;"
            else:
                query = f"""SELECT * FROM users WHERE {where_clause} AND deleted_at IS NULL;"""
            user_record = await self.fetchrow_or_404(query, *values)
            return self.get_user_from_record(user_record)
        else:
            raise UserAttrError(f"Allowed keys for using in ('id', 'username', 'email').")

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

    async def update(self, user_id: int, user: dict) -> GetUser:
        keys, values, indexes = self.data_from_dict(user)
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
