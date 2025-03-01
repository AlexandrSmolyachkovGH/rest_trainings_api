from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query, status

from trainings_app.schemas.memberships import GetMembership, CreateMembership, PutMembership, PatchMembership
from trainings_app.schemas.users import stuffer_roles
from trainings_app.repositories.memberships import MembershipRepository
from trainings_app.db.connection import get_repo
from trainings_app.auth.utils.jwt_utils import get_current_auth_user_with_role

router = APIRouter(
    prefix='/memberships',
    tags=['memberships'],
    dependencies=[Depends(get_current_auth_user_with_role(stuffer_roles))]
)


@router.get(
    path='/',
    response_model=list[GetMembership],
    description="Retrieve list of memberships",
    status_code=status.HTTP_200_OK,
)
async def get_memberships(
        access_level: Annotated[Optional[str], Query(description="Filter by access level")] = None,
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    return await repo.get_memberships(access_level)


@router.get(
    path='/{membership_id}',
    response_model=GetMembership,
    description="Retrieve the membership by ID",
    status_code=status.HTTP_200_OK,
)
async def get_membership(
        membership_id: Annotated[int, Path(gt=0)],
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    return await repo.get(membership_id)


@router.post(
    path='/',
    response_model=GetMembership,
    description="Create the membership",
    status_code=status.HTTP_201_CREATED,
)
async def create_membership(
        membership_obj: CreateMembership,
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    return await repo.create(membership_obj.dict())


@router.delete(
    path='/{membership_id}',
    response_model=GetMembership,
    description="Delete the membership",
    status_code=status.HTTP_200_OK,
)
async def delete_membership(
        membership_id: Annotated[int, Path(gt=0)],
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    return await repo.delete(membership_id)


@router.put(
    path='/{membership_id}',
    response_model=GetMembership,
    description="Complete update of the membership record",
    status_code=status.HTTP_200_OK,
)
async def put_membership(
        membership_id: Annotated[int, Path(gt=0)],
        data_for_update: PutMembership,
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    return await repo.update(membership_id, data_for_update.dict())


@router.patch(
    path='/{membership_id}',
    response_model=GetMembership,
    description="Partial update of the membership record",
    status_code=status.HTTP_200_OK,
)
async def patch_membership(
        membership_id: Annotated[int, Path(gt=0)],
        data_for_update: PatchMembership,
        repo: MembershipRepository = Depends(get_repo(MembershipRepository)),
):
    dict_for_update = data_for_update.model_dump(exclude_unset=True, exclude_defaults=True)
    return await repo.update(membership_id, dict_for_update)
