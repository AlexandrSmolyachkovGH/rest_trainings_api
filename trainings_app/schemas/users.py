from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, date
from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    TRAINER = 'TRAINER'
    STAFFER = 'STAFFER'
    SYSTEM = 'SYSTEM'
    ANALYST = 'ANALYST'
    OTHER = 'OTHER'


stuffer_roles = [RoleEnum.ADMIN, RoleEnum.SYSTEM, RoleEnum.ANALYST, RoleEnum.STAFFER, RoleEnum.TRAINER, RoleEnum.OTHER]
client_roles = [RoleEnum.USER]


class CreateUser(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=50,
        description='Unique valid username',
        example='john_doe_123',
    )
    password_hash: str = Field(
        min_length=2,
        max_length=255,
        description="Hashed password of the user",
        example="hashed_password_123",
    )
    email: EmailStr = Field(
        description='Unique valid email address',
        example='john.doe@example.com',
    )
    role: RoleEnum = Field(
        default=RoleEnum.USER,
        description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
        example='USER',
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="User registration date and time",
        example="2024-12-25 00:00:00",
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Date-time of the user's last login.",
        example='2024-12-25 00:00:00',
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Date of deletion of the user account.",
        example='2024-12-25 00:00:00',
    )


class GetUser(BaseModel):
    id: int = Field(
        ge=0,
        description="User ID",
        example=123,
    )
    username: str = Field(
        min_length=2,
        max_length=50,
        description='Unique valid username',
        example='john_doe_123',
    )
    password_hash: str = Field(
        min_length=2,
        max_length=255,
        description="Hashed password of the user",
        example="hashed_password_123",
    )
    email: EmailStr = Field(
        description='Unique valid email address',
        example='john.doe@example.com',
    )
    role: RoleEnum = Field(
        default=RoleEnum.USER,
        description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
        example='USER',
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="User registration date and time",
        example="2024-12-25 00:00:00",
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Date-time of the user's last login.",
        example='2024-12-25 00:00:00',
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Date of deletion of the user account.",
        example='2024-12-25 00:00:00',
    )


class PutUser(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=50,
        description='Unique valid username',
        example='john_doe_123',
    )
    password_hash: str = Field(
        min_length=2,
        max_length=255,
        description="Hashed password of the user",
        example="hashed_password_123",
    )
    email: EmailStr = Field(
        description='Unique valid email address',
        example='john.doe@example.com',
    )
    role: RoleEnum = Field(
        default=RoleEnum.USER,
        description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
        example='USER',
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="User registration date and time",
        example="2024-12-25 00:00:00",
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Date-time of the user's last login.",
        example='2024-12-25 00:00:00',
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Date of deletion of the user account.",
        example='2024-12-25 00:00:00',
    )


class PatchUser(BaseModel):
    username: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description='Unique valid username',
        example='john_doe_123',
    )
    password_hash: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
        description="Hashed password of the user",
        example="hashed_password_123",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description='Unique valid email address',
        example='john.doe@example.com',
    )
    role: Optional[RoleEnum] = Field(
        default=None,
        description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
        example='USER',
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="User registration date and time",
        example="2024-12-25 00:00:00",
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Date-time of the user's last login.",
        example='2024-12-25 00:00:00',
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Date of deletion of the user account.",
        example='2024-12-25 00:00:00',
    )


class FilterUser(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=0,
        description="User ID",
        example=123,
    )
    username: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description='Unique valid username',
        example='john_doe_123',
    )
    password_hash: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
        description="Hashed password of the user",
        example="hashed_password_123",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description='Unique valid email address',
        example='john.doe@example.com',
    )
    role: Optional[RoleEnum] = Field(
        default=None,
        description="User role in ['USER', 'TRAINER', 'ADMIN'] and etc.",
        example='USER',
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="User registration date and time",
        example="2024-12-25 00:00:00",
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Date-time of the user's last login.",
        example='2024-12-25 00:00:00',
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Date of deletion of the user account.",
        example='2024-12-25 00:00:00',
    )


class DateFilterUser(BaseModel):
    from_date: date
    to_date: date

    @field_validator("to_date")
    @classmethod
    def check_dates(cls, to_date, values):
        from_date = values.get("from_date")
        if from_date >= to_date:
            raise ValueError("from_date must be less then to_date")
        return to_date
