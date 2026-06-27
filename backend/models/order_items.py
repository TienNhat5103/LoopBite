from pydantic import BaseModel
from typing import Optional

class OrderItems(BaseModel):
    id: Optional[int] = None
    order_id: int
    food_id: int
    quantity: int
    total_price: float

    class Config:
        from_attributes = True