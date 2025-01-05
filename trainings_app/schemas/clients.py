from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from enum import Enum


class GenderEnum(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class CreateClient(BaseModel):
    user_id: int = Field(ge=0, description='User ID associated with the client')
    first_name: str = Field(min_length=2, max_length=50, description='The first name of the client', example='John')
    last_name: str = Field(min_length=2, max_length=80, description='The last name of the client', example='Doe')
    # Also in the user model
    email: Optional[EmailStr] = Field(description='A valid email address', example='john.doe@example.com')
    phone_number: str = Field(min_length=5, max_length=20, description='A phone number of the client',
                              example='+1234567890')
    # Also in the user model
    register_date: datetime = Field(default_factory=datetime.now, description='Date of the registration',
                                    example="2024-12-25 00:00:00")
    gender: GenderEnum = Field(description="Gender of client in ['MALE', 'FEMALE'].", example='MALE')
    date_of_birth: date = Field(description="Date of client birth", example="2024-12-25")
    weight_kg: Optional[float] = Field(default=None, ge=0, le=500,
                                       description='The weight of the client in kilograms (up to 2 decimal places)',
                                       example=70.5)
    height_cm: Optional[float] = Field(default=None, ge=0, le=500,
                                       description='The height of the client in centimeters (up to 2 decimal places)',
                                       example=175.2)
    membership_id: int = Field(description='The ID of the membership associated with the client.', example=123)


class GetClient(CreateClient):
    id: int = Field(ge=0, description='Client ID', example=123)
