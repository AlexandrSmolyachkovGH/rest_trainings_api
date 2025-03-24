from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, status, HTTPException

from trainings_app.auth.utils.jwt_utils import get_current_auth_user_with_role
from trainings_app.schemas.users import GetUser, CreateUser, PutUser, PatchUser, FilterUser, stuffer_roles, \
    client_roles, RoleEnum, DateFilterUser
from trainings_app.db.connection import get_repo
from trainings_app.repositories.users import UserRepository

router = APIRouter(prefix='/users', tags=['user'])


@router.get(
    path='/',
    response_model=list[GetUser],
    description="Retrieve list of users",
    status_code=status.HTTP_200_OK,
)
async def get_users(
        filter_model: FilterUser = Depends(),
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles)),
):
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    return await user_repo.get_users(filter_dict)


@router.get(
    path='/{user_id}',
    response_model=GetUser,
    description="Retrieve the user by ID",
    status_code=status.HTTP_200_OK,
)
async def get_user(
        user_id: Optional[int] = Path(gt=0, description="Filter by user ID"),
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    if user_id != user.id and user.role == RoleEnum.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No access to the specified user',
        )
    return await user_repo.get(user_id)


@router.get(
    path='/for-report/',
    response_model=list[GetUser],
    description="Retrieve list of users for a report",
    status_code=status.HTTP_200_OK,
)
async def get_new_users_for_report(
        filter_model: DateFilterUser = Depends(),
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
):
    filter_dict = filter_model.model_dump()
    return await user_repo.get_new_users_for_report(filter_dict)


@router.post(
    path='/',
    response_model=GetUser,
    description="Create the user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        user: CreateUser,
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
):
    return await user_repo.create(user.dict())


@router.delete(
    path='/{user_id}',
    response_model=GetUser,
    description="Delete the user",
    status_code=status.HTTP_200_OK,
)
async def delete_user(
        user_id: Annotated[int, Path(title='The ID of the user to delete', gt=0)],
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    if user_id != user.id and user.role == RoleEnum.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No access to the specified user',
        )
    return await user_repo.delete(user_id)


@router.put(
    path='/{user_id}',
    response_model=GetUser,
    description="Complete update of the user record",
    status_code=status.HTTP_200_OK,
)
async def put_user(
        user_id: Annotated[int, Path(gt=0)],
        user: PutUser,
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
        auth_user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    if user_id != auth_user.id and auth_user.role == RoleEnum.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No access to the specified user',
        )
    return await user_repo.update(user_id, user.dict())


@router.patch(
    path='/{user_id}',
    response_model=GetUser,
    description="Partial update of the user record",
    status_code=status.HTTP_200_OK,
)
async def patch_user(
        user_id: Annotated[int, Path(gt=0)],
        user: PatchUser,
        user_repo: UserRepository = Depends(get_repo(UserRepository)),
        auth_user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    if user_id != auth_user.id and auth_user.role == RoleEnum.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No access to the specified user',
        )
    return await user_repo.update(user_id, user.dict(exclude_defaults=True, exclude_unset=True))
