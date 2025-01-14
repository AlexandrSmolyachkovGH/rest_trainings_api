from fastapi import APIRouter, Path, Depends, status
from typing import Annotated

from trainings_app.db.connection import get_repo
from trainings_app.schemas.exercises import GetExercise, CreateExercise, PutExercise, PatchExercise, FilterExercise
from trainings_app.repositories.exercises import ExerciseRepository

router = APIRouter(prefix='/exercises', tags=['exercises'])


@router.get('/',
            response_model=list[GetExercise],
            description='Retrieve list of exercises',
            status_code=status.HTTP_200_OK)
async def get_exercises_list(
        filter_model: FilterExercise = Depends(),
        exercise_repo=Depends(get_repo(ExerciseRepository))
) -> list[GetExercise]:
    filter_dict = filter_model.model_dump(exclude_defaults=True) if filter_model else None
    exercises = await exercise_repo.get_exercises(filter_dict)
    return exercises


@router.get('/{exercise_id}',
            response_model=GetExercise,
            description='Retrieve the exercise',
            status_code=status.HTTP_200_OK)
async def get_exercise(exercise_id: int, exercise_repo=Depends(get_repo(ExerciseRepository))) -> GetExercise:
    exercise = await exercise_repo.get(exercise_id)
    return exercise


@router.post('/',
             response_model=GetExercise,
             description='Create the exercise',
             status_code=status.HTTP_201_CREATED)
async def create_exercise(model: CreateExercise, exercise_repo=Depends(get_repo(ExerciseRepository))) -> GetExercise:
    exercise = await exercise_repo.create(model.dict())
    return exercise


@router.put('/{exercise_id}',
            response_model=GetExercise,
            description='Complete update of the exercise record',
            status_code=status.HTTP_200_OK)
async def put_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        update_model: PutExercise,
        exercise_repo=Depends(get_repo(ExerciseRepository))
) -> GetExercise:
    updated_exercise = await exercise_repo.update(exercise_id, update_model.dict())
    return updated_exercise


@router.patch('/{exercise_id}',
              response_model=GetExercise,
              description='Partial update of the exercise record',
              status_code=status.HTTP_200_OK)
async def patch_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        update_model: PatchExercise,
        exercise_repo=Depends(get_repo(ExerciseRepository))
) -> GetExercise:
    update_dict = update_model.model_dump(exclude_defaults=True, exclude_unset=True)
    updated_exercise = await exercise_repo.update(exercise_id, update_dict)
    return updated_exercise


@router.delete('/{exercise_id}',
               response_model=GetExercise,
               description='Delete the exercise',
               status_code=status.HTTP_200_OK)
async def delete_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        exercise_repo=Depends(get_repo(ExerciseRepository))
) -> GetExercise:
    deleted_exercise = await exercise_repo.delete(exercise_id)
    return deleted_exercise
