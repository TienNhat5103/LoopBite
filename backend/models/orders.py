from pydantic import BaseModel
from typing import List, Optional

class Orders(BaseModel):
    id: Optional[int] = None  # Sơ đồ của bạn đang để kiểu int8 cho id đơn hàng
    user_id: str  # Liên kết tới uuid của profiles
    amount: float
    purchase_type: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
        
# Model đại diện cho từng món ăn được truyền lên trong giỏ hàng
class CartItemInput(BaseModel):
    food_id: int
    quantity: int

# Model chính nhận vào khi gọi API POST Create Order
class OrderCreateRequest(BaseModel):
    purchase_type: Optional[str] = "delivery"  # Mặc định là giao hàng, hoặc 'takeaway'...
    items: List[CartItemInput]
    
class UpdateStatusRequest(BaseModel):
    status: str