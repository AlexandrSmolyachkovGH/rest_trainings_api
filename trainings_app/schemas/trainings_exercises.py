from typing import Optional
from pydantic import BaseModel, Field


class CreateTrainingExercise(BaseModel):
    training_id: int = Field(description='ID of the associated training', example=1)
    exercise_id: int = Field(description='ID of the associated exercise', example=1)
    order_in_training: int = Field(description='Order of the exercise within the training session', example=1)
    sets: Optional[int] = Field(default=3, description='Number of sets for the exercise', example=3)
    reps: Optional[int] = Field(default=10, description='Number of repetitions per set', example=10)
    rest_time_sec: Optional[int] = Field(default=60, description='Rest time between sets in seconds', example=60)
    extra_weight: Optional[float] = Field(description='Extra weight for the exercise in kg', example=5.0)


class GetTrainingExercise(CreateTrainingExercise):
    id: int = Field(description='Unique ID')
