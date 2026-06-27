from pydantic import BaseModel
from typing import Optional

class Merchants(BaseModel):
    id: Optional[int] = None
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True