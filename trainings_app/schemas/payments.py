from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    EXPIRED = "EXPIRED"


class CreatePayment(BaseModel):
    client_id: int = Field(
        gt=0,
        description='Client ID associated with the payment',
        example=150,
    )
    membership_id: int = Field(
        gt=0,
        description="Membership ID associated with the payment",
        example=5,
    )
    payment_status: Optional[PaymentStatusEnum] = Field(
        default=None,
        description="Current payment status",
        example='PENDING',
    )


class GetPayment(BaseModel):
    id: int = Field(
        gt=0,
        description='ID of unique payment',
        example=35,
    )
    client_id: int = Field(
        gt=0,
        description='Client ID associated with the payment',
        example=150,
    )
    amount: float = Field(
        gt=0,
        description='Amount of money for the payment',
        example=599.99,
    )
    subscribe_type: str = Field(
        description='Type of subscription',
        example='STANDARD',
    )
    status: str = Field(
        description='Payment status',
        example='PAID',
    )
    timestamp: datetime = Field(
        description='Date and time of the payment',
        example='2025-06-15T14:30:00Z',
    )


class GetExtendedPaymentModel(BaseModel):
    payment_data: GetPayment = Field(
        description="Received payment model",
    )
    payment_link: str = Field(
        description="Link to the payment page",
        example='http://some_url/pay-page/?some_query_params',
    )
