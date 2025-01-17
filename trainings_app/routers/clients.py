from fastapi import APIRouter, Depends, Path, status
from typing import Annotated

from trainings_app.db.connection import get_repo
from trainings_app.schemas.clients import GetClient, CreateClient, PutClient, PatchClient, ClientFilters
from trainings_app.repositories.clients import ClientRepository

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/',
             response_model=GetClient,
             description='Create the client',
             status_code=status.HTTP_201_CREATED
             )
async def create_client(client: CreateClient, client_repo=Depends(get_repo(ClientRepository))) -> GetClient:
    client_dict = client.dict()
    created_client = await client_repo.create(client_dict)
    return created_client


@router.get('/{client_id}',
            response_model=GetClient,
            description='Retrieve the client by ID',
            status_code=status.HTTP_200_OK)
async def get_client(
        client_id: Annotated[int, Path(gt=0)],
        client_repo=Depends(get_repo(ClientRepository))
) -> GetClient:
    client = await client_repo.get(client_id)
    return client


@router.get('/',
            response_model=list[GetClient],
            description='Retrieve list of clients',
            status_code=status.HTTP_200_OK)
async def get_clients(
        filter_model: ClientFilters = Depends(),
        client_repo=Depends(get_repo(ClientRepository))):
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    clients = await client_repo.get_clients(filter_dict)
    return clients


@router.delete(path='/{client_id}',
               response_model=GetClient,
               description='Delete the client',
               status_code=status.HTTP_200_OK)
async def delete_client(
        client_id: Annotated[int, Path(gt=0)],
        client_repo=Depends(get_repo(ClientRepository))):
    client = await client_repo.delete(client_id)
    return client


@router.put(path='/{client_id}',
            response_model=GetClient,
            description='Complete update of the client record',
            status_code=status.HTTP_200_OK)
async def put_client(
        client_id: Annotated[int, Path(gt=0)], client_data: PutClient,
        client_repo=Depends(get_repo(ClientRepository))):
    updated_user = await client_repo.update(client_id, client_data.dict())
    return updated_user


@router.patch(path='/{client_id}',
              response_model=PatchClient,
              description='Partial update of the client record',
              status_code=status.HTTP_200_OK)
async def patch_client(
        client_id: Annotated[int, Path(gt=0)], client_data: PutClient,
        client_repo=Depends(get_repo(ClientRepository))):
    updated_user = await client_repo.update(client_id, client_data.dict(exclude_defaults=True, exclude_unset=True))
    return updated_user
