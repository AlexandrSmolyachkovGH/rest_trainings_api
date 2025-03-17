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
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description='Date and time of the payment',
        example='2025-06-15T14:30:00Z',
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
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description='Date and time of the payment',
        example='2025-06-15T14:30:00Z',
    )


class UpdatePayment(BaseModel):
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
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description='Date and time of the payment',
        example='2025-06-15T14:30:00Z',
    )


class FilterPayment(BaseModel):
    id: Optional[int] = Field(
        default=None,
        gt=0,
        description='ID of unique payment',
        example=35,
    )
    client_id: Optional[int] = Field(
        default=None,
        gt=0,
        description='Client ID associated with the payment',
        example=150,
    )
    membership_id: Optional[int] = Field(
        default=None,
        description="Membership ID associated with the payment",
        example=5,
    )
    payment_status: Optional[PaymentStatusEnum] = Field(
        default=None,
        description="Current payment status",
        example='PENDING',
    )
    timestamp: Optional[datetime] = Field(
        default=None,
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
