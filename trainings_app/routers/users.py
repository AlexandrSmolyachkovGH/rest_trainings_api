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
async def users(user_status: Annotated[
    Optional[Literal["active", "deleted"]],
    Query(description="Filter by user status")] = None,
                user_repo=Depends(get_repo(UserRepository))) -> list[GetUser]:
    users_list = await user_repo.get_users(user_status)
    return users_list


@router.get('/filter',
            response_model=GetUser,
            description="Retrieve the user by ID, Username or E-mail")
async def users(id: Optional[int] = Query(default=None, gt=0, description="Filter by user ID"),
                username: Optional[str] = Query(None, description="Filter by username"),
                email: Optional[str] = Query(None, description="Filter by email"),
                user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    try:
        user_attrs = {k: v for k, v in locals().items() if k in {"id", "username", "email"} and v is not None}
        user = await user_repo.get(user_attrs)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User was not found.")


@router.post('/',
             response_model=GetUser,
             description="Create the user")
async def users(user: CreateUser, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_dict = user.dict()
    created_user = await user_repo.create(user_dict)
    return created_user


@router.delete('/{user_id}',
               response_model=GetUser,
               description="Delete the user")
async def users(user_id: Annotated[int, Path(title='The ID of the user to delete', gt=0)],
                user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'id': user_id}
    deleted_user = await user_repo.delete(user_attr)
    return deleted_user


@router.put('/{user_id}',
            response_model=GetUser,
            description="Complete update of the user record")
async def users(user_id: int, user: UpdateUserPut,
                user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_user = await user_repo.update(user_id, user.dict())
    return updated_user


@router.patch('/{user_id}',
              response_model=GetUser,
              description="Partial update of the user record")
async def users(user_id: int, user: UpdateUserPatch,
                user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_user = await user_repo.update(user_id, user.dict(exclude_unset=True))
    return updated_user
