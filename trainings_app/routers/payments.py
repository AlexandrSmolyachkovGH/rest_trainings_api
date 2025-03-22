from fastapi import APIRouter, Depends, status

from trainings_app.auth.utils.jwt_utils import get_current_auth_user_with_role
from trainings_app.schemas.payments import (
    CreatePayment,
    GetExtendedPaymentModel,
)
from trainings_app.repositories.payments import PaymentRepository
from trainings_app.db.connection import get_repo
from trainings_app.schemas.users import GetUser, stuffer_roles, client_roles

router = APIRouter(prefix='/payments', tags=['payments'])


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
