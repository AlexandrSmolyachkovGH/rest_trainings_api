from fastapi import APIRouter, Path, Depends, status
from typing import Annotated

from trainings_app.db.connection import get_repo
from trainings_app.schemas.exercises import GetExercise, CreateExercise, PutExercise, PatchExercise, FilterExercise
from trainings_app.repositories.exercises import ExerciseRepository

router = APIRouter(prefix='/exercises', tags=['exercises'])


@router.get(
    path='/',
    response_model=list[GetExercise],
    description='Retrieve list of exercises',
    status_code=status.HTTP_200_OK,
)
async def get_exercises_list(
        filter_model: FilterExercise = Depends(),
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    return await exercise_repo.get_exercises(filter_dict)


@router.get(
    path='/{exercise_id}',
    response_model=GetExercise,
    description='Retrieve the exercise',
    status_code=status.HTTP_200_OK,
)
async def get_exercise(
        exercise_id: int,
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    return await exercise_repo.get(exercise_id)


@router.post(
    path='/',
    response_model=GetExercise,
    description='Create the exercise',
    status_code=status.HTTP_201_CREATED,
)
async def create_exercise(
        model: CreateExercise,
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    return await exercise_repo.create(model.dict())


@router.put(
    path='/{exercise_id}',
    response_model=GetExercise,
    description='Complete update of the exercise record',
    status_code=status.HTTP_200_OK,
)
async def put_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        update_model: PutExercise,
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    return await exercise_repo.update(exercise_id, update_model.dict())


@router.patch(
    path='/{exercise_id}',
    response_model=GetExercise,
    description='Partial update of the exercise record',
    status_code=status.HTTP_200_OK,
)
async def patch_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        update_model: PatchExercise,
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    update_dict = update_model.model_dump(exclude_defaults=True, exclude_unset=True)
    return await exercise_repo.update(exercise_id, update_dict)


@router.delete(
    path='/{exercise_id}',
    response_model=GetExercise,
    description='Delete the exercise',
    status_code=status.HTTP_200_OK,
)
async def delete_exercise(
        exercise_id: Annotated[int, Path(gt=0)],
        exercise_repo: ExerciseRepository = Depends(get_repo(ExerciseRepository)),
):
    return await exercise_repo.delete(exercise_id)
