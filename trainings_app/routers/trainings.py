from fastapi import APIRouter, Path, Depends, status
from typing import Annotated

from trainings_app.db.connection import get_repo
from trainings_app.schemas.exercises import ExerciseIDs
from trainings_app.schemas.trainings import CreateTraining, GetTraining, FilterTraining, PutTraining, PatchTraining, \
    CreateTrainingWithExerciseIDs
from trainings_app.repositories.trainings import TrainingRepository

router = APIRouter(prefix='/trainings', tags=['trainings'])


@router.get(
    path='/',
    response_model=list[GetTraining],
    description='Retrieve list of trainings',
    status_code=status.HTTP_200_OK,
)
async def get_trainings_list(
        filter_model: FilterTraining = Depends(),
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    filter_dict = filter_model.model_dump(exclude_defaults=True) if filter_model else None
    return await train_repo.get_trainings(filter_dict)


@router.get(
    path='/{train_id}',
    response_model=GetTraining,
    description='Retrieve the training',
    status_code=status.HTTP_200_OK,
)
async def get_training(
        train_id: Annotated[int, Path(gt=0)],
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.get(train_id)


@router.post(
    path='/',
    response_model=GetTraining,
    description='Create the training',
    status_code=status.HTTP_201_CREATED,
)
async def create_training(
        create_model: CreateTraining,
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.create(create_model.dict())


@router.post(
    path='/exercises',
    response_model=GetTraining,
    description='Create the training',
    status_code=status.HTTP_201_CREATED,
)
async def create_training_with_exercises(
        train_model: CreateTraining,
        ex_ids_model: ExerciseIDs,
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.create_train_with_ex(train_model.dict(), ex_ids_model.exercises)


@router.post(
    path='/exercise-ids',
    response_model=GetTraining,
    description='Create the training with exercises',
    status_code=status.HTTP_201_CREATED,
)
async def create_training_with_exercise_ids(
        train_model: CreateTrainingWithExerciseIDs,
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.create_train_with_exercise_ids(train_model.dict())


@router.put(
    path='/{train_id}',
    response_model=GetTraining,
    description='Complete update of the training record',
    status_code=status.HTTP_200_OK,
)
async def put_training(
        train_id: Annotated[int, Path(gt=0)],
        update_model: PutTraining,
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.update(train_id, update_model.dict())


@router.patch(
    path='/{train_id}',
    response_model=GetTraining,
    description='Partial update of the training record',
    status_code=status.HTTP_200_OK,
)
async def patch_training(
        train_id: Annotated[int, Path(gt=0)],
        update_model: PatchTraining,
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    update_dict = update_model.model_dump(exclude_defaults=True, exclude_unset=True)
    return await train_repo.update(train_id, update_dict)


@router.delete(
    path='/{train_id}',
    response_model=GetTraining,
    description='Delete the training',
    status_code=status.HTTP_200_OK,
)
async def delete_training(
        train_id: Annotated[int, Path(gt=0)],
        train_repo: TrainingRepository = Depends(get_repo(TrainingRepository)),
):
    return await train_repo.delete(train_id)
