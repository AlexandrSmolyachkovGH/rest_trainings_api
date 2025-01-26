from typing import Optional
from pydantic import BaseModel, Field


class CreateTrainingPlanTraining(BaseModel):
    training_id: int = Field(
        ge=0,
        description='Training ID',
        example=10,
    )
    training_plan_id: int = Field(
        ge=0,
        description='Training ID',
        example=10,
    )


class GetTrainingPlanTraining(BaseModel):
    id: Optional[int] = Field(
        description='Unique ID',
    )
    training_id: int = Field(
        ge=0,
        description='Training ID',
        example=10,
    )
    training_plan_id: int = Field(
        ge=0,
        description='Training ID',
        example=10,
    )
