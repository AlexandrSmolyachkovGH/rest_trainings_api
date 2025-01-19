from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query, status

from trainings_app.schemas.memberships import GetMembership, CreateMembership, PutMembership, PatchMembership
from trainings_app.repositories.memberships import MembershipRepository
from trainings_app.db.connection import get_repo

router = APIRouter(prefix='/memberships', tags=['memberships'])


@router.get('/',
            response_model=list[GetMembership],
            description="Retrieve list of memberships",
            status_code=status.HTTP_200_OK)
async def get_memberships(
        access_level: Annotated[Optional[str], Query(description="Filter by access level")] = None,
        repo=Depends(get_repo(MembershipRepository))
) -> list[GetMembership]:
    membership_list = await repo.get_memberships(access_level)
    return membership_list


@router.get('/{membership_id}',
            response_model=GetMembership,
            description="Retrieve the membership by ID",
            status_code=status.HTTP_200_OK)
async def get_membership(
        membership_id: Annotated[int, Path(gt=0)],
        repo=Depends(get_repo(MembershipRepository))
) -> GetMembership:
    membership_data = await repo.get(membership_id)
    return membership_data


@router.post('/',
             response_model=GetMembership,
             description="Create the membership",
             status_code=status.HTTP_201_CREATED)
async def create_membership(
        membership_obj: CreateMembership,
        repo=Depends(get_repo(MembershipRepository))
) -> GetMembership:
    membership_dict = membership_obj.dict()
    membership_data = await repo.create(membership_dict)
    return membership_data


@router.delete('/{membership_id}',
               response_model=GetMembership,
               description="Delete the membership",
               status_code=status.HTTP_200_OK)
async def delete_membership(
        membership_id: Annotated[int, Path(gt=0)],
        repo=Depends(get_repo(MembershipRepository))
) -> GetMembership:
    membership_data = await repo.delete(membership_id)
    return membership_data


@router.put('/{membership_id}',
            response_model=GetMembership,
            description="Complete update of the membership record",
            status_code=status.HTTP_200_OK)
async def put_membership(
        membership_id: Annotated[int, Path(gt=0)], data_for_update: PutMembership,
        repo=Depends(get_repo(MembershipRepository))
) -> GetMembership:
    membership_data = await repo.update(membership_id, data_for_update.dict())
    return membership_data


@router.patch('/{membership_id}',
              response_model=GetMembership,
              description="Partial update of the membership record",
              status_code=status.HTTP_200_OK)
async def patch_membership(
        membership_id: Annotated[int, Path(gt=0)], data_for_update: PatchMembership,
        repo=Depends(get_repo(MembershipRepository))
) -> GetMembership:
    dict_for_update = data_for_update.model_dump(exclude_unset=True, exclude_defaults=True)
    membership_data = await repo.update(membership_id, dict_for_update)
    return membership_data
