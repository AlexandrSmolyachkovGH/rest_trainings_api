from typing import Annotated
from fastapi import APIRouter, Depends, Path, status

from trainings_app.schemas.payments import (
    FilterPayment,
    GetPayment,
    CreatePayment,
    UpdatePayment,
    GetExtendedPaymentModel,
)
from trainings_app.repositories.payments import PaymentRepository
from trainings_app.db.connection import get_repo
from trainings_app.auth.utils.jwt_utils import get_current_auth_user_with_role
from trainings_app.schemas.users import GetUser, stuffer_roles, client_roles

router = APIRouter(prefix='/payments', tags=['payments'])


@router.get(
    path='/',
    response_model=list[GetPayment],
    description="Retrieve list of payments",
    status_code=status.HTTP_200_OK,
)
async def get_payments(
        filter_model: FilterPayment = Depends(),
        repo: PaymentRepository = Depends(get_repo(PaymentRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),

):
    filter_dict = filter_model.model_dump(exclude_defaults=True, exclude_unset=True) if filter_model else None
    return await repo.get_payments(filter_dict)


@router.get(
    path='/{payment_id}',
    response_model=GetPayment,
    description="Retrieve the payment by ID",
    status_code=status.HTTP_200_OK,
)
async def get_payment(
        payment_id: int = Path(gt=0, description="Filter by payment ID"),
        repo: PaymentRepository = Depends(get_repo(PaymentRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    return await repo.get(payment_id)


@router.post(
    path='/',
    response_model=GetExtendedPaymentModel,
    description="Create the payment",
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
        payment: CreatePayment,
        repo: PaymentRepository = Depends(get_repo(PaymentRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    return await repo.create(payment.dict())


@router.delete(
    path='/{payment_id}',
    response_model=GetPayment,
    description="Delete the payment",
    status_code=status.HTTP_200_OK,
)
async def delete_payment(
        payment_id: Annotated[int, Path(title='The ID of the payment to delete', gt=0)],
        repo: PaymentRepository = Depends(get_repo(PaymentRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    return await repo.delete(payment_id)


@router.put(
    path='/{payment_id}',
    response_model=GetPayment,
    description="Complete update of the payment record",
    status_code=status.HTTP_200_OK,
)
async def put_payment(
        payment_id: Annotated[int, Path(gt=0)],
        payment: UpdatePayment,
        repo: PaymentRepository = Depends(get_repo(PaymentRepository)),
        user: GetUser = Depends(get_current_auth_user_with_role(allowed_roles=stuffer_roles + client_roles)),
):
    return await repo.update(payment_id, payment.dict())
