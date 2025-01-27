from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ComplexityEnum(str, Enum):
    BEGINNER = 'BEGINNER'
    NOVICE = 'NOVICE'
    INTERMEDIATE = 'INTERMEDIATE'
    ADVANCED = 'ADVANCED'
    EXPERT = 'EXPERT'
    MASTER = 'MASTER'


class MuscleGroupEnum(str, Enum):
    CHEST = 'CHEST'
    BACK = 'BACK'
    LEGS = 'LEGS'
    ARMS = 'ARMS'
    CORE = 'CORE'
    SHOULDERS = 'SHOULDERS'
    BUTTOCKS = 'BUTTOCKS'
    CALVES = 'CALVES'
    NECK = 'NECK'
    HIPS = 'HIPS'
    FULL_BODY = 'FULL_BODY'
    OTHER = 'OTHER'


class ExerciseIDs(BaseModel):
    exercises: Optional[list] = Field(
        default=None,
        description='Unique exercise IDs',
        example='[1, 12, 5, 81]',
    )


class CreateExercise(BaseModel):
    title: str = Field(
        max_length=50,
        description='Unique title of the exercise',
        example='Push-ups',
    )
    description: Optional[str] = Field(
        default=None,
        description='Detailed description of the exercise',
        example='A basic exercise for arms',
    )
    muscle_group: Optional[MuscleGroupEnum] = Field(
        default=None, description='Target muscle group for the exercise',
        example='ARMS',
    )
    equipment_required: bool = Field(
        default=False,
        description='Indicates if the exercise requires equipment',
        example=False,
    )
    complexity_lvl: ComplexityEnum = Field(
        default=ComplexityEnum.BEGINNER,
        description='Complexity level of the exercise',
        example='BEGINNER',
    )


class GetExercise(BaseModel):
    id: int = Field(
        description='Unique ID for the exercise',
        example=1,
    )
    title: str = Field(
        max_length=50,
        description='Unique title of the exercise',
        example='Push-ups',
    )
    description: str = Field(
        description='Detailed description of the exercise',
        example='A basic exercise for arms',
    )
    muscle_group: Optional[MuscleGroupEnum] = Field(
        description='Target muscle group for the exercise',
        example='ARMS',
    )
    equipment_required: bool = Field(
        description='Indicates if the exercise requires equipment',
        example=False,
    )
    complexity_lvl: ComplexityEnum = Field(
        description='Complexity level of the exercise',
        example='BEGINNER',
    )


class PutExercise(BaseModel):
    title: str = Field(
        max_length=50,
        description='Unique title of the exercise',
        example='Push-ups',
    )
    description: Optional[str] = Field(
        default=None,
        description='Detailed description of the exercise',
        example='A basic exercise for arms',
    )
    muscle_group: Optional[MuscleGroupEnum] = Field(
        default=None,
        description='Target muscle group for the exercise',
        example='ARMS',
    )
    equipment_required: bool = Field(
        default=False,
        description='Indicates if the exercise requires equipment',
        example=False,
    )
    complexity_lvl: ComplexityEnum = Field(
        default=ComplexityEnum.BEGINNER,
        description='Complexity level of the exercise',
        example='BEGINNER',
    )


class PatchExercise(BaseModel):
    title: Optional[str] = Field(
        default=None,
        max_length=50,
        description='Unique title of the exercise',
        example='Push-ups',
    )
    description: Optional[str] = Field(
        default=None,
        description='Detailed description of the exercise',
        example='A basic exercise for arms',
    )
    muscle_group: Optional[MuscleGroupEnum] = Field(
        default=None,
        description='Target muscle group for the exercise',
        example='ARMS',
    )
    equipment_required: Optional[bool] = Field(
        default=False,
        description='Indicates if the exercise requires equipment',
        example=False,
    )
    complexity_lvl: Optional[ComplexityEnum] = Field(
        default=ComplexityEnum.BEGINNER,
        description='Complexity level of the exercise',
        example='BEGINNER',
    )


class FilterExercise(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description='Unique ID for the exercise',
        example=1,
    )
    title: Optional[str] = Field(
        default=None,
        max_length=50,
        description='Unique title of the exercise',
        example='Push-ups',
    )
    description: Optional[str] = Field(
        default=None,
        description='Detailed description of the exercise',
        example='A basic exercise for arms',
    )
    muscle_group: Optional[MuscleGroupEnum] = Field(
        default=None,
        description='Target muscle group for the exercise',
        example='ARMS',
    )
    equipment_required: Optional[bool] = Field(
        default=False,
        description='Indicates if the exercise requires equipment',
        example=False,
    )
    complexity_lvl: Optional[ComplexityEnum] = Field(
        default=ComplexityEnum.BEGINNER,
        description='Complexity level of the exercise',
        example='BEGINNER',
    )
