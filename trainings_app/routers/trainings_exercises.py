from fastapi import APIRouter, Path, Depends, status
from typing import Annotated

from trainings_app.db.connection import get_repo
from trainings_app.schemas.trainings_exercises import CreateTrainingExercise, GetTrainingExercise, \
    FilterTrainingExercise, PatchTrainingExercise, PutTrainingExercise
from trainings_app.repositories.trainings_exercises import TrainingExerciseRepository

router = APIRouter(prefix='/trainings-exercises', tags=['trainings-exercises'])


@router.post(
    path='/',
    response_model=GetTrainingExercise,
    description='Add the training-exercise record',
    status_code=status.HTTP_201_CREATED,
)
async def create_training_exercise(
        create_model: CreateTrainingExercise,
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    return await repo.create(create_model.dict())


@router.get(
    path='/{training_id}/{exercise_id}',
    response_model=GetTrainingExercise,
    description="Retrieve the training-exercise record",
    status_code=status.HTTP_200_OK,
)
async def get_training_exercise(
        training_id: Annotated[int, Path(gt=0, description="training_id")],
        exercise_id: Annotated[int, Path(gt=0, description="exercise_id")],
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    return await repo.get(training_id, exercise_id)


@router.get(
    path='/',
    response_model=list[GetTrainingExercise],
    description="Retrieve training-exercise records",
    status_code=status.HTTP_200_OK,
)
async def get_trainings_exercises(
        filter_model: FilterTrainingExercise = Depends(),
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    filter_dict = filter_model.model_dump(exclude_defaults=True) if filter_model else None
    return await repo.get_trainings_exercises(filter_dict)


@router.delete(
    path='/{training_id}/{exercise_id}',
    response_model=GetTrainingExercise,
    description="Delete the training-exercise record",
    status_code=status.HTTP_200_OK,
)
async def delete_training_exercise(
        training_id: Annotated[int, Path(gt=0, description="training_id")],
        exercise_id: Annotated[int, Path(gt=0, description="exercise_id")],
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    return await repo.delete(training_id, exercise_id)


@router.put(
    path='/{training_id}/{exercise_id}',
    response_model=GetTrainingExercise,
    description='Complete update of the training-exercise record',
    status_code=status.HTTP_200_OK,
)
async def put_training_exercise(
        training_id: Annotated[int, Path(gt=0, description="training_id")],
        exercise_id: Annotated[int, Path(gt=0, description="exercise_id")],
        update_model: PutTrainingExercise,
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    return await repo.update(training_id, exercise_id, update_model.dict())


@router.patch(
    path='/{training_id}/{exercise_id}',
    response_model=GetTrainingExercise,
    description='Partial update of the training-exercise record',
    status_code=status.HTTP_200_OK,
)
async def patch_training_exercise(
        training_id: Annotated[int, Path(gt=0, description="training_id")],
        exercise_id: Annotated[int, Path(gt=0, description="exercise_id")],
        update_model: PatchTrainingExercise,
        repo: TrainingExerciseRepository = Depends(get_repo(TrainingExerciseRepository)),
):
    update_dict = update_model.model_dump(exclude_defaults=True, exclude_unset=True)
    return await repo.update(training_id, exercise_id, update_dict)
