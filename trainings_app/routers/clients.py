from fastapi import APIRouter, Depends, Path, status, HTTPException
from typing import Annotated

from trainings_app.auth.utils.jwt_utils import get_current_token_payload, get_current_auth_user
from trainings_app.db.connection import get_repo
from trainings_app.schemas.clients import GetClient, CreateClient, PutClient, PatchClient, ClientFilters
from trainings_app.repositories.clients import ClientRepository

router = APIRouter(
    prefix='/clients',
    tags=['clients'],
    dependencies=[Depends(get_current_token_payload),],
)


@router.post(
    path='/',
    response_model=GetClient,
    description='Create the client',
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
        client: CreateClient,
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
        payload: dict = Depends(get_current_token_payload),
):
    if client.user_id != payload.get('sub') and payload.get('role') == 'USER':
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid ID of the user: {payload.get('sub')}.",
        )
    return await client_repo.create(client.model_dump(exclude_unset=True, exclude_defaults=True))


@router.get(
    path='/{client_id}',
    response_model=GetClient,
    description='Retrieve the client by ID',
    status_code=status.HTTP_200_OK,
)
async def get_client(
        client_id: Annotated[int, Path(gt=0)],
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
):
    return await client_repo.get(client_id)


@router.get(
    path='/',
    response_model=list[GetClient],
    description='Retrieve list of clients',
    status_code=status.HTTP_200_OK,
)
async def get_clients(
        filter_model: ClientFilters = Depends(),
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
):
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    return await client_repo.get_clients(filter_dict)


@router.delete(
    path='/{client_id}',
    response_model=GetClient,
    description='Delete the client',
    status_code=status.HTTP_200_OK,
)
async def delete_client(
        client_id: Annotated[int, Path(gt=0)],
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
):
    return await client_repo.delete(client_id)


@router.put(
    path='/{client_id}',
    response_model=GetClient,
    description='Complete update of the client record',
    status_code=status.HTTP_200_OK,
)
async def put_client(
        client_id: Annotated[int, Path(gt=0)],
        client_data: PutClient,
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
):
    return await client_repo.update(client_id, client_data.dict())


@router.patch(
    path='/{client_id}',
    response_model=GetClient,
    description='Partial update of the client record',
    status_code=status.HTTP_200_OK,
)
async def patch_client(
        client_id: Annotated[int, Path(gt=0)],
        client_data: PatchClient,
        client_repo: ClientRepository = Depends(get_repo(ClientRepository)),
):
    return await client_repo.update(client_id, client_data.dict(exclude_defaults=True, exclude_unset=True))
