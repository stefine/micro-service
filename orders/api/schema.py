from pydantic import BaseModel, conint, Extra, validator, conlist
from typing import Optional, List
from enum import Enum
from uuid import UUID
from datetime import datetime


class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class Status(Enum):
    created = 'created'
    paid = 'paid'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, le=100000)] = 1

    class Config:
        extra = Extra.forbid

    @validator('quantity')
    def quantity_non_nullable(cls, value):
        assert value is not None, 'quantity may not be None'
        return value


class GetOrderSchema(BaseModel):
    id: UUID
    created: datetime
    status: Status
    order: OrderItemSchema

    class Config:
        extra = Extra.forbid


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]


class CreateOrderSchema(BaseModel):
    order: OrderItemSchema

    class Config:
        extra = Extra.forbid
