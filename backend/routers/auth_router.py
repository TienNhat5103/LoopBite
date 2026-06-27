from fastapi import APIRouter, HTTPException, status, Header, Depends
from database import supabase
from models import UserRegister, UserLogin  # <-- Thêm Depends vào đây
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <-- Thêm 2 class này


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
security = HTTPBearer()

# 1. ĐĂNG KÝ (Sign Up)
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister):
    try:
        # Đăng ký tài khoản vào hệ thống Auth của Supabase
        # Trigger dưới DB sẽ tự động lấy thông tin full_name bọc vào profiles
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "full_name": user_data.full_name
                }
            }
        })
        return {
            "message": "Đăng ký thành công! Vui lòng kiểm tra email để xác thực (nếu có bật)",
            "user_id": response.user.id if response.user else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đăng ký: {str(e)}")

# 2. ĐĂNG NHẬP (Sign In) -> Lấy Access Token
@router.post("/login")
def login_user(user_data: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        
        # Trả về access_token để Client đính kèm vào các request sau
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sai tài khoản hoặc mật khẩu: {str(e)}")

# 3. CHECK AUTH ID (Lấy id người dùng hiện tại từ Token)
@router.get("/me")
def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Lấy token thô đã được FastAPI tự động bóc tách (bỏ sẵn chữ Bearer)
    token = credentials.credentials
    
    try:
        # Gửi token lên Supabase để quét thông tin
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # Gọi xuống bảng profiles để lấy thông tin chi tiết
        profile_response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        if not profile_response.data:
            raise HTTPException(status_code=404, detail="Không tìm thấy profile tương ứng với User ID này")
            
        return {
            "auth_id": user_id,
            "profile_details": profile_response.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token không hợp lệ hoặc đã hết hạn: {str(e)}")
   
# Endpoint dành cho việc xóa tài khoản dựa trên user_id cụ thể truyền vào
@router.delete("/delete-user/{user_id}")
def delete_user_by_id(user_id: str):
    try:
        # Sử dụng quyền Admin API của Supabase SDK để xóa tài khoản trong auth.users bằng ID
        # Cơ chế ON DELETE CASCADE dưới DB sẽ tự động dọn dẹp bảng profiles tương ứng
        supabase.auth.admin.delete_user(user_id)
        
        return {
            "status": "Thành công",
            "message": f"Tài khoản có ID {user_id} đã bị xóa hoàn toàn khỏi auth.users và public.profiles."
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Lỗi khi xóa tài khoản có ID {user_id}: {str(e)}"
        )