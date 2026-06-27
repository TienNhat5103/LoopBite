from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class Food(BaseModel):
    id: Optional[int] = None
    merchant_id: int
    name: str
    category: Optional[str] = None
    price: float  # Map với kiểu numeric trong DB
    quantity: int
    status: str
    expiry_time: Optional[datetime] = None
    best_before_time: Optional[time] = None

    class Config:
        from_attributes = True
        
class FoodUpdate(BaseModel):
    price: float
    quantity: int


    class Config:
        from_attributes = True