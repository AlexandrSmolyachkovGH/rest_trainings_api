from datetime import datetime
from trainings_app.schemas.users import CreateUser, GetUser
from typing import Any
from fastapi import HTTPException, status


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def is_username_or_email_taken(self, username: str, email: str) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE username = $1 OR email = $2
            )
        """
        result = await self.db.fetchval(query, username, email)
        return result

    @staticmethod
    async def get_user_from_record(record: dict) -> GetUser:
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
    async def check_delete_status(record: dict):
        if record['deleted_at'] is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Deleted User')

    async def create_user(self, user: CreateUser) -> GetUser:
        self.is_username_or_email_taken(user.username, user.email)
        query = """
                INSERT INTO users (username, password_hash, email, role, created_at, last_login, deleted_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *;
            """
        user_params = (
            user.username,
            user.password_hash,
            user.email,
            user.role,
            user.created_at,
            user.last_login,
            user.deleted_at
        )
        user_record = await self.db.fetchval(query, *user_params)
        # check the hint
        return self.get_user_from_record(user_record)

    async def get_user_by_id(self, user_id: int) -> GetUser:
        query = """SELECT * FROM users WHERE id = $1;"""
        user_record = await self.db.fetchrow(query, user_id)
        return self.get_user_from_record(user_record)

    async def get_user_by_username(self, username: str) -> GetUser:
        query = """SELECT * FROM users WHERE username = $1;"""
        user_record = await self.db.fetchrow(query, username)
        return self.get_user_from_record(user_record)

    async def delete_user(self, user_attr: Any[int, str]) -> GetUser:
        if isinstance(user_attr, int):
            query = """
                UPDATE users
                SET deleted_at = $1
                WHERE id = $2
                RETURNING *;
            """
            user_record = await self.db.fetchrow(query, datetime.now(), user_attr)
        else:
            query = """
                UPDATE users
                SET deleted_at = $1
                WHERE username = $2
                RETURNING *;
            """
            user_record = await self.db.fetchrow(query, datetime.now(), user_attr)
        return self.get_user_from_record(user_record)
