from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    TRAINER = 'TRAINER'
    STAFFER = 'STAFFER'
    SYSTEM = 'SYSTEM'
    ANALYST = 'ANALYST'
    OTHER = 'OTHER'


class CreateUser(BaseModel):
    username: str = Field(min_length=2, max_length=50, description='Unique valid username', example='john_doe_123')
    password_hash: str = Field(min_length=2, max_length=255, description="Hashed password of the user",
                               example="hashed_password_123")
    email: EmailStr = Field(description='Unique valid email address', example='john.doe@example.com')
    role: RoleEnum = Field(default=RoleEnum.USER, description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
                           example='USER')
    created_at: datetime = Field(default_factory=datetime.now, description="User registration date and time",
                                 example="2024-12-25 00:00:00")
    last_login: Optional[datetime] = Field(default=None,
                                           description="Date-time of the user's last login.",
                                           example='2024-12-25 00:00:00')
    deleted_at: Optional[datetime] = Field(default=None,
                                           description="Date of deletion of the user account.",
                                           example='2024-12-25 00:00:00')


class GetUser(CreateUser):
    id: int = Field(ge=0, description="User ID", example=123)


class PutUser(CreateUser):
    ...


class PatchUser(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=50, description='Unique valid username',
                                    example='john_doe_123')
    password_hash: Optional[str] = Field(None, min_length=2, max_length=255, description="Hashed password of the user",
                                         example="hashed_password_123")
    email: Optional[EmailStr] = Field(None, description='Unique valid email address', example='john.doe@example.com')
    role: Optional[RoleEnum] = Field(None, description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
                                     example='USER')
    created_at: Optional[datetime] = Field(None, description="User registration date and time",
                                           example="2024-12-25 00:00:00")
    last_login: Optional[datetime] = Field(None, description="Date-time of the user's last login.",
                                           example='2024-12-25 00:00:00')
    deleted_at: Optional[datetime] = Field(None, description="Date of deletion of the user account.",
                                           example='2024-12-25 00:00:00')

