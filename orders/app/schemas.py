from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class DishInOrder(BaseModel):
    dish_id: int
    quantity: int


class OrderCreate(BaseModel):
    dishes: List[DishInOrder]
    special_requests: str


class OrderStatus(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True
