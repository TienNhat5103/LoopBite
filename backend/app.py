from fastapi import FastAPI
from contextlib import asynccontextmanager
from middlewares.cors import apply_cors_middleware
from routers import api_router
from database import supabase
from fastapi.security import HTTPBearer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Đoạn code này sẽ chạy NGAY KHI SERVER KHỞI ĐỘNG ---
    print("\n" + "="*50)
    print("Đang kiểm tra kết nối tới Supabase...")
    try:
        # Gửi một request cực nhẹ tới hệ thống Auth của Supabase để check connection
        supabase.auth.get_session()
        print("👉 KẾT NỐI SUPABASE: THÀNH CÔNG! 🎉")
    except Exception as e:
        print("❌ KẾT NỐI SUPABASE: THẤT BẠI! 🛠️")
        print(f"Chi tiết lỗi: {e}")
    print("="*50 + "\n")
    
    yield

def create_app() -> FastAPI:
    # Gắn lifespan vào đây để FastAPI kích hoạt khi chạy uvicorn
    app = FastAPI(lifespan=lifespan) 
    security = HTTPBearer()
    app = apply_cors_middleware(app)
    app.include_router(api_router)

    return app
    