from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class AccessLevelEnum(str, Enum):
    LIMIT = 'LIMIT'
    STANDARD = 'STANDARD'
    PREMIUM = 'PREMIUM'
    VIP = 'VIP'
    FAMILY = 'FAMILY'
    TRIAL = 'TRIAL'
    DAY_PASS = 'DAY_PASS'
    WEEK_PASS = 'WEEK_PASS'
    GUEST = 'GUEST'
    CORPORATE = 'CORPORATE'
    DISCOUNT = 'DISCOUNT'
    OTHER = 'OTHER'


class CreateMembership(BaseModel):
    access_level: AccessLevelEnum = Field(
        default=AccessLevelEnum.STANDARD,
        description='Allowed membership access',
        example='VIP',
    )
    description: Optional[str] = Field(
        default=None,
        description='Membership card description, including services, benefits, and additional information.',
        example='Full access to all services',
    )
    price: float = Field(
        ge=0,
        description='Membership price in local currency',
        example='149.99',
    )


class GetMembership(BaseModel):
    id: int = Field(
        ge=0,
        description='Membership ID',
        example=123,
    )
    access_level: AccessLevelEnum = Field(
        description='Allowed membership access',
        example='VIP',
    )
    description: Optional[str] = Field(
        description='Membership card description, including services, benefits, and additional information.',
        example='Full access to all services',
    )
    price: float = Field(
        ge=0,
        description='Membership price in local currency',
        example='149.99',
    )


class PutMembership(BaseModel):
    access_level: AccessLevelEnum = Field(
        default=AccessLevelEnum.STANDARD,
        description='Allowed membership access',
        example='VIP',
    )
    description: Optional[str] = Field(
        description='Membership card description, including services, benefits, and additional information.',
        example='Full access to all services',
    )
    price: float = Field(
        ge=0,
        description='Membership price in local currency',
        example='149.99',
    )


class PatchMembership(BaseModel):
    access_level: Optional[AccessLevelEnum] = Field(
        default=AccessLevelEnum.STANDARD,
        description='Allowed membership access',
        example='VIP',
    )
    description: Optional[str] = Field(
        default=None,
        description='Membership card description, including services, benefits, and additional information.',
        example='Full access to all services',
    )
    price: Optional[float] = Field(
        default=None,
        ge=0,
        description='Membership price in local currency',
        example='149.99',
    )
