from fastapi import APIRouter
from .food_router import router as food_router  
from .merchant_router import router as merchant_router

api_router = APIRouter()

# Đăng ký router đồ ăn vào hệ thống API chính
api_router.include_router(merchant_router)
api_router.include_router(food_router)