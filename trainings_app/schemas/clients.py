from typing import Optional
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class GenderEnum(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class ClientStatusEnum(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ON_HOLD = 'ON_HOLD'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    UPCOMING = 'UPCOMING'


class CreateClient(BaseModel):
    user_id: int = Field(
        ge=0,
        description='User ID associated with the client',
    )
    membership_id: int = Field(
        ge=0,
        description='The ID of the membership associated with the client.',
        example=123,
    )
    first_name: str = Field(
        min_length=2,
        max_length=50,
        description='The first name of the client',
        example='John',
    )
    last_name: str = Field(
        min_length=2,
        max_length=80,
        description='The last name of the client',
        example='Doe',
    )
    phone_number: str = Field(
        min_length=5,
        max_length=20,
        description='A phone number of the client',
        example='+1234567890',
    )
    gender: GenderEnum = Field(
        description="Gender of client in ['MALE', 'FEMALE'].",
        example='MALE',
    )
    date_of_birth: date = Field(
        description="Date of client birth",
        example="2024-12-25",
    )
    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The weight of the client in kilograms (up to 2 decimal places)',
        example=70.5,
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The height of the client in centimeters (up to 2 decimal places)',
        example=175.2,
    )
    status: ClientStatusEnum = Field(
        default=ClientStatusEnum.ACTIVE,
        description="Client activity status",
        example='INACTIVE',
    )


class GetClient(BaseModel):
    id: int = Field(
        ge=0,
        description='Client ID',
        example=123,
    )
    user_id: int = Field(
        ge=0,
        description='User ID associated with the client',
    )
    membership_id: int = Field(
        ge=0,
        description='The ID of the membership associated with the client.',
        example=123,
    )
    first_name: str = Field(
        min_length=2,
        max_length=50,
        description='The first name of the client',
        example='John',
    )
    last_name: str = Field(
        min_length=2,
        max_length=80,
        description='The last name of the client',
        example='Doe',
    )
    phone_number: str = Field(
        min_length=5,
        max_length=20,
        description='A phone number of the client',
        example='+1234567890',
    )
    gender: GenderEnum = Field(
        description="Gender of client in ['MALE', 'FEMALE'].",
        example='MALE',
    )
    date_of_birth: date = Field(
        description="Date of client birth",
        example="2024-12-25",
    )
    weight_kg: float = Field(
        ge=0,
        le=500,
        description='The weight of the client in kilograms (up to 2 decimal places)',
        example=70.5,
    )
    height_cm: float = Field(
        ge=0,
        le=500,
        description='The height of the client in centimeters (up to 2 decimal places)',
        example=175.2,
    )
    status: ClientStatusEnum = Field(
        description="Client activity status",
        example='INACTIVE',
    )


class PutClient(BaseModel):
    membership_id: int = Field(
        ge=0,
        description='The ID of the membership associated with the client.',
        example=123,
    )
    first_name: str = Field(
        min_length=2,
        max_length=50,
        description='The first name of the client',
        example='John',
    )
    last_name: str = Field(
        min_length=2,
        max_length=80,
        description='The last name of the client',
        example='Doe',
    )
    phone_number: str = Field(
        min_length=5,
        max_length=20,
        description='A phone number of the client',
        example='+1234567890',
    )
    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The weight of the client in kilograms (up to 2 decimal places)',
        example=70.5,
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The height of the client in centimeters (up to 2 decimal places)',
        example=175.2,
    )
    status: ClientStatusEnum = Field(
        default=ClientStatusEnum.ACTIVE,
        description="Client activity status",
        example='INACTIVE',
    )


class PatchClient(BaseModel):
    user_id: Optional[int] = Field(
        default=None,
        ge=0,
        description='User ID associated with the client',
    )
    membership_id: Optional[int] = Field(
        ge=0,
        default=None,
        description='The ID of the membership associated with the client.',
        example=123,
    )
    first_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description='The first name of the client',
        example='John',
    )
    last_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=80,
        description='The last name of the client',
        example='Doe',
    )
    phone_number: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=20,
        description='A phone number of the client',
        example='+1234567890',
    )
    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The weight of the client in kilograms (up to 2 decimal places)',
        example=70.5,
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The height of the client in centimeters (up to 2 decimal places)',
        example=175.2,
    )
    status: Optional[ClientStatusEnum] = Field(
        default=None,
        description="Client activity status",
        example='INACTIVE',
    )


class ClientFilters(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=0,
        description='Client ID',
        example=123,
    )
    user_id: Optional[int] = Field(
        default=None,
        ge=0,
        description='User ID associated with the client',
    )
    membership_id: Optional[int] = Field(
        ge=0,
        default=None,
        description='The ID of the membership associated with the client.',
        example=123,
    )
    first_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description='The first name of the client',
        example='John',
    )
    last_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=80,
        description='The last name of the client',
        example='Doe',
    )
    phone_number: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=20,
        description='A phone number of the client',
        example='+1234567890',
    )
    gender: Optional[GenderEnum] = Field(
        default=None,
        description="Gender of client in ['MALE', 'FEMALE'].",
        example='MALE',
    )
    date_of_birth: Optional[date] = Field(
        default=None,
        description="Date of client birth",
        example="2024-12-25",
    )
    weight_kg: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The weight of the client in kilograms (up to 2 decimal places)',
        example=70.5,
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=0,
        le=500,
        description='The height of the client in centimeters (up to 2 decimal places)',
        example=175.2,
    )
    status: Optional[ClientStatusEnum] = Field(
        default=None,
        description="Client activity status",
        example='INACTIVE',
    )
