from fastapi import APIRouter
from .food_router import router as food_router
from .merchant_router import router as merchant_router
from .profile_router import router as profile_router
from .order_router import router as order_router
from .order_item_router import router as order_item_router
from .auth_router import router as auth_router
from .search_engines import router as search_router


api_router = APIRouter()

# Đăng ký tập trung tất cả các endpoint
api_router.include_router(food_router)
api_router.include_router(merchant_router)
api_router.include_router(profile_router)
api_router.include_router(order_router)
api_router.include_router(order_item_router)
api_router.include_router(auth_router)
api_router.include_router(food_router)
api_router.include_router(search_router)

