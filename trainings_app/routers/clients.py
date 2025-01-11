from datetime import date

from fastapi import APIRouter, Depends, Path, Query
from trainings_app.db.connection import get_repo
from typing import Annotated, Optional
from trainings_app.schemas.clients import GetClient, CreateClient, ClientStatusEnum, PutClient, PatchClient
from trainings_app.repositories.clients import ClientRepository

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/',
             response_model=GetClient,
             description='Create the client')
async def create_client(client: CreateClient,
                        client_repo=Depends(get_repo(ClientRepository))
                        ) -> GetClient:
    client_dict = client.dict()
    created_client = await client_repo.create(client_dict)
    return created_client


@router.get('/{client_id}',
            response_model=GetClient,
            description='Retrieve the client by ID')
async def get_client_by_id(client_id: Annotated[int, Path(gt=0)],
                           client_repo=Depends(get_repo(ClientRepository))) -> GetClient:
    client = await client_repo.get(client_id)
    return client


@router.get('/',
            response_model=list[GetClient],
            description='Retrieve list of clients')
async def get_clients(id: Optional[int] = Query(None, ge=0, description='Filter by Client ID'),
                      user_id: Optional[int] = Query(None, ge=0, description='Filter by User ID'),
                      phone_number: Optional[str] = Query(None, min_length=5, max_length=20,
                                                          description='Filter by phone number of the client'),
                      status: Optional[ClientStatusEnum] = Query(None, description="Filter by client status"),
                      client_repo=Depends(get_repo(ClientRepository))):
    filter_params = {key: value for key, value in locals().items() if
                     value is not None and key in ['id', 'user_id', 'phone_number', 'status']}
    clients = await client_repo.get_clients(filter_params if filter_params else None)
    return clients


@router.delete(path='/{client_id}',
               response_model=GetClient,
               description='Delete the client')
async def delete_client(client_id: Annotated[int, Path(gt=0)],
                        client_repo=Depends(get_repo(ClientRepository))):
    client = await client_repo.delete(client_id)
    return client


@router.put(path='/{client_id}',
            response_model=GetClient,
            description='Complete update of the client record')
async def put_client(client_id: Annotated[int, Path(gt=0)],
                     client_data: PutClient,
                     client_repo=Depends(get_repo(ClientRepository))):
    updated_user = await client_repo.update(client_id, client_data.dict())
    return updated_user


@router.patch(path='/{client_id}',
              response_model=PatchClient,
              description='Partial update of the client record')
async def patch_client(client_id: Annotated[int, Path(gt=0)],
                       client_data: PutClient,
                       client_repo=Depends(get_repo(ClientRepository))):
    updated_user = await client_repo.update(client_id, client_data.dict())
    return updated_user
