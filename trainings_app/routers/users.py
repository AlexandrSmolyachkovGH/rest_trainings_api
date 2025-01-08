from typing import Annotated, Optional, Literal
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status

from trainings_app.schemas.users import GetUser, CreateUser, UpdateUserPut, UpdateUserPatch
from trainings_app.db.connection import get_repo
from trainings_app.repositories.user_repository import UserRepository
from trainings_app.exceptions.user import UserNotFoundError

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/',
            response_model=list[GetUser],
            description="Retrieve list of users")
async def get_users(user_status: Annotated[
                    Optional[Literal["active", "deleted"]],
                    Query(description="Filter by user status")] = None,
                    user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    users = await user_repo.get_users(user_status)
    return users


@router.get('/{user_id}',
            response_model=GetUser,
            description="Retrieve the user by ID")
async def get_user_by_id(user_id: Annotated[int, Path(gt=0)],
                         user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    try:
        user_attr = {'id': user_id}
        user = await user_repo.get(user_attr)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {user_id} was not found.")


@router.get('/{username}',
            response_model=GetUser,
            description="Retrieve the user by Username")
async def get_user_by_username(username: Annotated[str, Path(min_length=3, max_length=50)],
                               user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    try:
        user_attr = {'username': username}
        user = await user_repo.get(user_attr)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with Username: {username} was not found.")


@router.get('/{email}',
            response_model=GetUser,
            description="Retrieve the user by Email")
async def get_user_by_email(email: Annotated[str, Path(min_length=5, max_length=100)],
                            user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    try:
        user_attr = {'email': email}
        user = await user_repo.get(user_attr)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with E-mail: {email} was not found.")


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
