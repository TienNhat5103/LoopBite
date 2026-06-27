from fastapi import APIRouter
from .food_router import router as food_router  # Import router vừa viết từ file food_router.py

api_router = APIRouter()

# Đăng ký router đồ ăn vào hệ thống API chính
api_router.include_router(food_router)