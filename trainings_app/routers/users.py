from fastapi import APIRouter, Depends, Path, Query
from trainings_app.schemas.users import GetUser, CreateUser, UpdateUserPut, UpdateUserPatch
from trainings_app.db.connection import get_repo
from trainings_app.repositories.user_repository import UserRepository
from typing import Annotated

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/', response_model=list[GetUser])
async def get_users(user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    users = await user_repo.get_active_users()
    return users


@router.get('/id', response_model=GetUser)
async def get_user_by_id(user_id: Annotated[int, Query(gt=0)], user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'id': user_id}
    user = await user_repo.get(user_attr)
    return user


@router.get('/username', response_model=GetUser)
async def get_user_by_username(username: Annotated[str, Query(min_length=3, max_length=50)],
                               user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'username': username}
    user = await user_repo.get(user_attr)
    return user


@router.get('/email', response_model=GetUser)
async def get_user_by_email(email: Annotated[str, Query(min_length=5, max_length=100)],
                            user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'email': email}
    user = await user_repo.get(user_attr)
    return user


@router.get('/deleted', response_model=list[GetUser])
async def get_deleted_users(user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    users = await user_repo.get_deleted_users()
    return users


@router.post('/', response_model=GetUser)
async def create_user(user: CreateUser, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_dict = user.dict()
    created_user = await user_repo.create(user_dict)
    return created_user


@router.delete('/id/{user_id}', response_model=GetUser)
async def delete_user_by_id(user_id: Annotated[int, Path(title='The ID of the user to delete', gt=0)],
                            user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'id': user_id}
    deleted_user = await user_repo.delete(user_attr)
    return deleted_user


@router.delete('/username/{username}', response_model=GetUser)
async def delete_user_by_username(username: Annotated[str, Path(title='The Username of the user to delete')],
                                  user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'username': username}
    deleted_user = await user_repo.delete(user_attr)
    return deleted_user


@router.put('/user/{user_id}', response_model=GetUser)
async def put_user(user_id: int, user: UpdateUserPut,
                   user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_user = await user_repo.update(user_id, user.dict())
    return updated_user


@router.patch('/user/{user_id}', response_model=GetUser)
async def patch_user(user_id: int, user: UpdateUserPatch,
                     user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_user = await user_repo.update(user_id, user.dict(exclude_unset=True))
    return updated_user
