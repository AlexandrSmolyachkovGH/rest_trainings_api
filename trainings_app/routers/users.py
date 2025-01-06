from fastapi import APIRouter, Depends
from trainings_app.schemas.users import GetUser, CreateUser, UpdateUserPut, UpdateUserPatch
from trainings_app.db.connection import get_repo
from trainings_app.repositories.user_repository import UserRepository

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/', response_model=list[GetUser])
async def get_users(user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    users = await user_repo.get_active_users()
    return users


@router.get('/user/{user_attr}', response_model=GetUser)
async def get_user(user_attr: int | str, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user = await user_repo.get_user_by_id(user_attr)
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


@router.delete('/', response_model=GetUser)
async def delete_user(user_attr: dict, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user = await user_repo.delete(user_attr)
    return user


@router.put('/user/{user_attr}', response_model=GetUser)
async def put_user(user_attr: int | str, user: UpdateUserPut,
                   user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user = await user_repo.update(user_attr, user.dict())
    return user


@router.patch('/user/{user_attr}', response_model=GetUser)
async def patch_user(user_attr: int | str, user: UpdateUserPatch,
                     user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user = await user_repo.update(user_attr, user.dict(exclude_unset=True))
    return user
