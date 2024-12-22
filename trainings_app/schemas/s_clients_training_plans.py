from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CreateClientTrainingPlan(BaseModel):
    client_id: int = Field(description='ID of the Client', example=12)
    training_plan_id: int = Field(description='ID of the training plan', example=90)
    pinned_at: Optional[datetime] = Field(default_factory=datetime.now, description='Date of the pin',
                                          example='2023-12-31T23:59:59')


class GetClientTrainingPlan(CreateClientTrainingPlan):
    id: int = Field(description='Unique ID')
