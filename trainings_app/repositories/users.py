import json
from typing import Optional
from datetime import datetime
from pydantic import ValidationError

from trainings_app.custom_loggers.console_debug import console_logger
from trainings_app.db.fields.users import UserFields
from trainings_app.schemas.users import GetUser
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import ConvertRecordError
from trainings_app.custom_loggers.repositories import repo_logger
from trainings_app.utils.password_hashing import hash_password


class UserRepository(BaseRepository):
    fields = UserFields

    @staticmethod
    def __get_user_from_record(record: dict) -> GetUser:
        """Retrieve GetUser model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetUser(**record)
        except ValidationError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail=f"{str(e)}")

    async def create(self, user: dict) -> GetUser:
        user['password_hash'] = hash_password(user['password_hash'])
        keys, values, indexes = self.data_from_dict(user)
        query = f"""
            INSERT INTO users ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        user_record = await self.fetchrow_or_404(query, *values)
        return self.__get_user_from_record(user_record)

    async def get(self, user_id: int) -> GetUser:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM users
            WHERE id = $1;
        """
        user_record = await self.fetchrow_or_404(query, user_id)
        return self.__get_user_from_record(user_record)

    async def delete(self, user_id: int) -> GetUser:
        query = f"""
            UPDATE users
            SET deleted_at = $1
            WHERE id = $2 AND deleted_at IS NULL
            RETURNING {self.fields.get_fields_str()};
        """
        user_record = await self.fetchrow_or_404(query, datetime.now(), user_id)
        return self.__get_user_from_record(user_record)

    async def get_users(self, filters: Optional[dict]) -> list[GetUser]:
        values = []
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM users
        """
        if filters:
            keys, values, indexes = self.data_from_dict(filters)
            where_clause = ' AND '.join([f"{key} = ${ind}" for key, ind in zip(keys, indexes)])
            query += f"""
                WHERE {where_clause}
            """
        query += ";"
        user_records = await self.conn.fetch(query, *values)
        return [GetUser(**record) for record in user_records]

    async def get_new_users_for_report(self, filters: dict) -> str:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM users
            WHERE created_at BETWEEN $1 AND $2;
        """
        try:
            user_records = await self.conn.fetch(query, *filters.values())
        except Exception as e:
            console_logger.info(f"{e}")
        user_records_list = [GetUser(**record) for record in user_records]
        return user_records_list

    async def update(self, user_id: int, update_data: dict) -> GetUser:
        if update_data.get('password_hash'):
            update_data['password_hash'] = hash_password(update_data['password_hash'])
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise ValidationError("Invalid update data")
        values.append(user_id)
        set_clause = ", ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
        query = f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ${len(indexes) + 1} AND deleted_at IS NULL
            RETURNING {self.fields.get_fields_str()}; 
        """
        user_record = await self.fetchrow_or_404(query, *values)
        return self.__get_user_from_record(user_record)
