from pydantic import BaseModel, Field
from typing import Optional
from datetime import time, datetime, timedelta  # <-- Đảm bảo import 'time' ở đây

# Khai báo hàm factory mặc định trả về kiểu 'time' (chỉ lấy giờ hiện tại)
def get_current_time():
    return datetime.now().time()

def get_current_time_plus_one_hour():
    return (datetime.now() + timedelta(hours=1)).time()

class Merchants(BaseModel):
    id: Optional[int] = None
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # ÉP VỀ KIỂU time (Chỉ có Giờ:Phút:Giây) để khớp với data thực tế '09:12:08' dưới DB
    order_start_time: Optional[time] = Field(default_factory=get_current_time)
    order_end_time: Optional[time] = Field(default_factory=get_current_time_plus_one_hour)

    class Config:
        from_attributes = True