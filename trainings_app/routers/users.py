from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, status

from trainings_app.schemas.users import GetUser, CreateUser, PutUser, PatchUser, FilterUser
from trainings_app.db.connection import get_repo
from trainings_app.repositories.users import UserRepository

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/',
            response_model=list[GetUser],
            description="Retrieve list of users",
            status_code=status.HTTP_200_OK)
async def get_users(
        filter_model: FilterUser = Depends(),
        user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    got_records = await user_repo.get_users(filter_dict)
    return got_records


@router.get('/{user_id}',
            response_model=GetUser,
            description="Retrieve the user by ID",
            status_code=status.HTTP_200_OK)
async def get_user(
        user_id: Optional[int] = Path(gt=0, description="Filter by user ID"),
        user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    got_record = await user_repo.get(user_id)
    return got_record


@router.post('/',
             response_model=GetUser,
             description="Create the user",
             status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_dict = user.dict()
    created_record = await user_repo.create(user_dict)
    return created_record


@router.delete('/{user_id}',
               response_model=GetUser,
               description="Delete the user",
               status_code=status.HTTP_200_OK)
async def delete_user(
        user_id: Annotated[int, Path(title='The ID of the user to delete', gt=0)],
        user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    record = await user_repo.delete(user_id)
    return record


@router.put('/{user_id}',
            response_model=GetUser,
            description="Complete update of the user record",
            status_code=status.HTTP_200_OK)
async def put_user(
        user_id: int, user: PutUser,
        user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_record = await user_repo.update(user_id, user.dict())
    return updated_record


@router.patch('/{user_id}',
              response_model=GetUser,
              description="Partial update of the user record",
              status_code=status.HTTP_200_OK)
async def patch_user(
        user_id: int, user: PatchUser,
        user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_record = await user_repo.update(user_id, user.dict(exclude_defaults=True, exclude_unset=True))
    return updated_record
