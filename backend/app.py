import sys
sys.stdout.reconfigure(encoding='utf-8')
from fastapi import FastAPI
from contextlib import asynccontextmanager
from middlewares.cors import apply_cors_middleware
from routers import api_router
from database import supabase
from fastapi.security import HTTPBearer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Äoáº¡n code nÃ y sáº½ cháº¡y NGAY KHI SERVER KHá»žI Äá»˜NG ---
    print("\n" + "="*50)
    print("Äang kiá»ƒm tra káº¿t ná»‘i tá»›i Supabase...")
    try:
        # Gá»­i má»™t request cá»±c nháº¹ tá»›i há»‡ thá»‘ng Auth cá»§a Supabase Ä‘á»ƒ check connection
        supabase.auth.get_session()
        print("ðŸ‘‰ Káº¾T Ná»I SUPABASE: THÃ€NH CÃ”NG! ðŸŽ‰")
    except Exception as e:
        print("âŒ Káº¾T Ná»I SUPABASE: THáº¤T Báº I! ðŸ› ï¸")
        print(f"Chi tiáº¿t lá»—i: {e}")
    print("="*50 + "\n")
    
    yield

def create_app() -> FastAPI:
    # Gáº¯n lifespan vÃ o Ä‘Ã¢y Ä‘á»ƒ FastAPI kÃ­ch hoáº¡t khi cháº¡y uvicorn
    app = FastAPI(lifespan=lifespan) 
    security = HTTPBearer()
    app = apply_cors_middleware(app)
    app.include_router(api_router)

    return app
    
