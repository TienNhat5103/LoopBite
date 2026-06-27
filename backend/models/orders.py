from pydantic import BaseModel
from typing import Optional

class Orders(BaseModel):
    id: Optional[int] = None  # Sơ đồ của bạn đang để kiểu int8 cho id đơn hàng
    user_id: str  # Liên kết tới uuid của profiles
    amount: float
    purchase_type: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True