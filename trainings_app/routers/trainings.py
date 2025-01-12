from fastapi import APIRouter, Path, Query, Depends
from typing import Annotated, Optional

from trainings_app.db.connection import get_repo
from trainings_app.schemas.trainings import CreateTraining, GetTraining, TrainingTypeEnum, IntensityEnum, \
    FilterTraining, PutTraining, PatchTraining
from trainings_app.exceptions.trainings import TrainingsAttrError, TrainingNotFoundError, ConvertTrainingRecordError
from trainings_app.repositories.trainings import TrainingRepository

router = APIRouter(prefix='/trainings', tags=['trainings'])


@router.get('/',
            response_model=list[GetTraining],
            description='Retrieve list of trainings')
async def get_trainings_list(
        filter_model: FilterTraining = Depends(),
        train_repo=Depends(get_repo(TrainingRepository))
) -> list[GetTraining]:
    filter_dict = filter_model.model_dump(exclude_defaults=True) if filter_model else None
    trainings = await train_repo.get_trainings(filter_dict if filter_dict else None)
    return trainings


@router.get('/{train_id}',
            response_model=GetTraining,
            description='Retrieve the training')
async def get_training(
        train_id: Annotated[int, Path(gt=0)],
        train_repo=Depends(get_repo(TrainingRepository))
) -> GetTraining:
    training = await train_repo.get(train_id)
    return training


@router.post('/',
             response_model=GetTraining,
             description='Create the training')
async def create_training(
        create_model: CreateTraining,
        train_repo=Depends(get_repo(TrainingRepository))
) -> GetTraining:
    training = await train_repo.create(create_model.dict())
    return training


@router.put('/{train_id}',
            response_model=GetTraining,
            description='Complete update of the training record')
async def put_training(
        train_id: Annotated[int, Path(gt=0)],
        update_model: PutTraining,
        train_repo=Depends(get_repo(TrainingRepository))
) -> GetTraining:
    training = train_repo.put(train_id, update_model.dict())
    return training


@router.patch('/{train_id}',
            response_model=GetTraining,
            description='Partial update of the training record')
async def patch_training(
        train_id: Annotated[int, Path(gt=0)],
        update_model: PatchTraining,
        train_repo=Depends(get_repo(TrainingRepository))
) -> GetTraining:
    training = train_repo.patch(train_id, update_model.dict())
    return training


@router.delete('/{train_id}',
               response_model=GetTraining,
               description='Delete the training')
async def delete_training(
        train_id: Annotated[int, Path(gt=0)],
        train_repo=Depends(get_repo(TrainingRepository))
) -> GetTraining:
    training = train_repo.delete(train_id)
    return training
