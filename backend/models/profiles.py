from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Profiles(BaseModel):
    id: str  # Định dạng UUID từ auth.users sẽ lưu ở dạng chuỗi
    created_at: Optional[datetime] = None
    role: Optional[str] = "customer"
    full_name: Optional[str] = None

    class Config:
        from_attributes = True