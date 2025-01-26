from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TrainingPlanStatusEnum(str, Enum):
    PREPARED = 'PREPARED'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    DELAYED = 'DELAYED'


class CreateTrainingPlan(BaseModel):
    user_id: int = Field(
        gt=0,
        description='User ID associated with the training plan',
        example=42,
    )
    title: str = Field(
        max_length=200,
        description='Title of the training plan',
        example='My Training Plan',
    )
    description: Optional[str] = Field(
        description='Detailed description of the training plan',
        example='A plan for muscle building.',
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description='Timestamp when the plan was created',
        example='2024-12-25T12:00:00',
    )
    status: TrainingPlanStatusEnum = Field(
        default=TrainingPlanStatusEnum.ACTIVE,
        description='Status of the training plan',
        example='ACTIVE',
    )


class GetTrainingPlan(BaseModel):
    id: int = Field(
        gt=0,
        description='Unique training plan ID',
        example=1,
    )
    user_id: int = Field(
        gt=0,
        description='User ID associated with the training plan',
        example=42,
    )
    title: str = Field(
        max_length=200,
        description='Title of the training plan',
        example='My Training Plan',
    )
    description: Optional[str] = Field(
        description='Detailed description of the training plan',
        example='A plan for muscle building.',
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description='Timestamp when the plan was created',
        example='2024-12-25T12:00:00',
    )
    status: TrainingPlanStatusEnum = Field(
        default=TrainingPlanStatusEnum.ACTIVE,
        description='Status of the training plan',
        example='ACTIVE',
    )
