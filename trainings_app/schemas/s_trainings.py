from typing import Optional
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class TrainingTypeEnum(str, Enum):
    CARDIO = 'CARDIO'
    STRENGTH = 'STRENGTH'
    FLEXIBILITY = 'FLEXIBILITY'
    BALANCE = 'BALANCE'
    HIIT = 'HIIT'
    YOGA = 'YOGA'
    PILATES = 'PILATES'
    ENDURANCE = 'ENDURANCE'
    CROSSFIT = 'CROSSFIT'
    FUNCTIONAL = 'FUNCTIONAL'
    REHABILITATION = 'REHABILITATION'
    DANCE = 'DANCE'
    SWIMMING = 'SWIMMING'
    OTHER = 'OTHER'


class IntensityEnum(str, Enum):
    VERY_LOW = 'VERY_LOW'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY_HIGH'
    EXTREME = 'EXTREME'


class CreateTraining(BaseModel):
    client_id: int = Field(description='Client ID associated with the training', example=123)
    training_type: Optional[TrainingTypeEnum] = Field(description='Type of training', example='CARDIO')
    title: str = Field(min_length=1, max_length=200, description='Title of the training', example='Morning Cardio')
    intensity: Optional[IntensityEnum] = Field(description='Intensity level of the training', example='MEDIUM')
    duration_min: int = Field(default=45, description='Duration of the training session in minutes', example=45)
    date: Optional[date] = Field(description='Date of the training session', example='2024-12-25')
    description: Optional[str] = Field(description='Detailed description of the training',
                                       example='A cardio session focusing on endurance.')


class GetTraining(CreateTraining):
    id: int = Field(ge=0, description='Unique training ID', example=123)
