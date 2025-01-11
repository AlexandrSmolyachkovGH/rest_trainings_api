from typing import Annotated, Optional, Literal
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from datetime import datetime

from trainings_app.schemas.users import GetUser, CreateUser, PutUser, PatchUser
from trainings_app.db.connection import get_repo
from trainings_app.repositories.users import UserRepository
from trainings_app.exceptions.user import UserNotFoundError

router = APIRouter(prefix='/users', tags=['user'])


@router.get('/',
            response_model=list[GetUser],
            description="Retrieve list of users")
async def get_users(id: Optional[int] = Query(None, gt=0, description='Filter by user ID'),
                    username: Optional[str] = Query(None, description='Filter by Username'),
                    email: Optional[str] = Query(None, description='Filter by E-mail'),
                    role: Optional[str] = Query(None, description='Filter by User role'),
                    deleted_at: Optional[datetime] = Query(None, description="Filter by Delete status"),
                    user_repo=Depends(get_repo(UserRepository))):
    filter_dict = {key: value for key, value in locals().items() if
                   value is not None and key in ['id', 'username', 'email', 'role', 'deleted_at']}
    got_records = await user_repo.get_users(filter_dict if filter_dict else None)
    return got_records


@router.get('/{user_id}',
            response_model=GetUser,
            description="Retrieve the user by ID")
async def get_user(user_id: Optional[int] = Path(gt=0, description="Filter by user ID"),
                   user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    got_record = await user_repo.get(user_id)
    return got_record


@router.post('/',
             response_model=GetUser,
             description="Create the user")
async def create_user(user: CreateUser, user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_dict = user.dict()
    created_record = await user_repo.create(user_dict)
    return created_record


@router.delete('/{user_id}',
               response_model=GetUser,
               description="Delete the user")
async def delete_user(user_id: Annotated[int, Path(title='The ID of the user to delete', gt=0)],
                      user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    user_attr = {'id': user_id}
    record = await user_repo.delete(user_attr)
    return record


@router.put('/{user_id}',
            response_model=GetUser,
            description="Complete update of the user record")
async def put_user(user_id: int, user: PutUser,
                   user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_record = await user_repo.update(user_id, user.dict())
    return updated_record


@router.patch('/{user_id}',
              response_model=GetUser,
              description="Partial update of the user record")
async def patch_user(user_id: int, user: PatchUser,
                     user_repo=Depends(get_repo(UserRepository))) -> GetUser:
    updated_record = await user_repo.update(user_id, user.dict(exclude_unset=True))
    return updated_record
