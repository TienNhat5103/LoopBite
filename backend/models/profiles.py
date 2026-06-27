from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Model cũ giữ nguyên
class Profiles(BaseModel):
    id: str  
    email: Optional[EmailStr] = None
    created_at: Optional[datetime] = None
    role: Optional[str] = "customer"
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- THÊM 2 MODEL MỚI NÀY VÀO DƯỚI CÙNG FILE ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True