from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status

from trainings_app.db.fields.users import UserFields
from trainings_app.schemas.users import CreateUser, GetUser
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import ConvertRecordError, RecordNotFoundError, AttrError
from trainings_app.logging.repositories import repo_logger


class UserRepository(BaseRepository):
    fields = UserFields

    @staticmethod
    def get_user_from_record(record: dict) -> GetUser:
        """Retrieve GetUser model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, model_name="GetUser", error_detail="No record found to convert")
        try:
            return GetUser(**record)
        except Exception as e:
            repo_logger.error(f"Convert to model Error: {e}")
            raise ConvertRecordError(record=record, model_name="GetUser", error_detail="Invalid data for conversion")

    async def create(self, user: CreateUser) -> GetUser:
        keys, values, indexes = self.data_from_dict(user)
        query = f"""
            INSERT INTO users ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        try:
            user_record = await self.db.fetchrow(query, *values)
        except Exception as e:
            repo_logger.error(f"Creation Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed. Please try again later."
            )
        return self.get_user_from_record(user_record)

    async def get(self, user_id: int) -> GetUser:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM users
            WHERE id = $1;
        """
        user_record = await self.fetchrow_or_404(query, user_id)
        return self.get_user_from_record(user_record)

    async def delete(self, user_id: int) -> GetUser:
        query = f"""
            UPDATE users
            SET deleted_at = $1
            WHERE id = $2 AND deleted_at IS NULL
            RETURNING {self.fields.get_fields_str()};
        """
        user_record = await self.fetchrow_or_404(query, datetime.now(), user_id)
        return self.get_user_from_record(user_record)

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
        user_records = await self.db.fetch(query, *values)
        if not user_records:
            repo_logger.error(f"No relevant records Error")
            raise RecordNotFoundError(f"No relevant records")
        return [GetUser(**record) for record in user_records]

    async def update(self, user_id: int, update_data: dict) -> GetUser:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise AttrError("Invalid update data")
        values.append(user_id)
        set_clause = ", ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
        query = f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ${len(indexes) + 1} AND deleted_at IS NULL
            RETURNING {self.fields.get_fields_str()}; 
        """
        user_record = await self.fetchrow_or_404(query, *values)
        return self.get_user_from_record(user_record)
