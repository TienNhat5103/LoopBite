from time import time
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Optional

def get_now():
    return datetime.now()

# Hàm bổ trợ lấy thời gian hiện tại cộng thêm 1 giờ
def get_now_plus_one_hour():
    return datetime.now() + timedelta(hours=1)

class Merchants(BaseModel):
    id: Optional[int] = None
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Sử dụng default_factory để tự động sinh thời gian tại thời điểm gọi API
    order_start_time: Optional[datetime] = Field(default_factory=get_now)
    order_end_time: Optional[datetime] = Field(default_factory=get_now_plus_one_hour)

    class Config:
        from_attributes = True