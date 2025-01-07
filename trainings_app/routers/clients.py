from fastapi import APIRouter, Depends, Path, Query
from trainings_app.db.connection import get_repo
from typing import Annotated
from trainings_app.schemas.clients import GetClient, CreateClient, GenderEnum
from trainings_app.repositories.client_repository import ClientRepository

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/', response_model=GetClient)
async def create_user(user: CreateClient, client_repo=Depends(get_repo(ClientRepository))) -> GetClient:
    client_dict = user.dict()
    created_client = await client_repo.create(client_dict)
    return created_client


@router.get('/id', response_model=GetClient)
async def get_client_by_id(client_id: Annotated[int, Query(gt=0)],
                           client_repo=Depends(get_repo(ClientRepository))) -> GetClient:
    client_attr = {'id': client_id}
    client = await client_repo.get(client_attr)
    return client
