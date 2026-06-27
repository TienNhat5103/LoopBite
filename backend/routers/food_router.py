from fastapi import APIRouter, HTTPException, status, Depends  # Thêm Depends vào đây
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Thêm 2 class bảo mật
from typing import List
from database import supabase,SUPABASE_KEY, SUPABASE_URL, create_client
from models import Food, FoodUpdate  
import random  

router = APIRouter(
    prefix="/api/v1/food",
    tags=["Food CRUD Operations"]
)

# Khởi tạo cơ chế bắt Token ổ khóa cho riêng file này
security = HTTPBearer()

# Hàm bổ trợ (Helper function) dùng để ép kiểm tra quyền Merchant
def verify_merchant_role(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        # 1. Gọi Supabase Auth giải mã token lấy user_id
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # 2. Quét bảng profiles xem tài khoản này giữ role gì
        profile_response = supabase.table("profiles").select("role").eq("id", user_id).execute()
        
        if not profile_response.data:
            raise HTTPException(status_code=404, detail="Không tìm thấy profile của người dùng này")
            
        current_role = profile_response.data[0].get("role")
        
        # 3. CHẶN QUYỀN: Nếu không phải merchant, từ chối truy cập ngay lập tức
        if current_role != "merchant":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Quyền truy cập bị từ chối! Chỉ tài khoản chủ cửa hàng (merchant) mới có quyền thực hiện hành động này."
            )
            
        return user_id # Trả về id nếu hợp lệ (phòng trường hợp sau này cần dùng)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Xác thực token thất bại: {str(e)}")


# 1. READ ALL - Ai cũng xem được (Không cần bảo mật)
@router.get("/", response_model=List[Food])
def get_all_food():
    try:
        # Thay thế ascending=True bằng desc=False để xếp từ nhỏ đến lớn theo ID
        response = (
            supabase
            .table("food")
            .select("*")
            .order("id", desc=False)  # <-- ĐỔI THÀNH desc=False 
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Lỗi lấy danh sách món: {str(e)}"
        )
# 2. READ BY ID - Ai cũng xem được (Không cần bảo mật)
@router.get("/{food_id}", response_model=Food)
def get_food_by_id(food_id: int):
    try:
        response = supabase.table("food").select("*").eq("id", food_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Không tìm thấy món ăn có ID = {food_id}"
            )
        return response.data[0]
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

# 3. CREATE - Nhập món ăn mới (Tùy Quân chọn, hiện tại đang để trống tự do, có thể thêm kiểm tra quyền nếu cần)
@router.post("/", response_model=Food, status_code=201)
def create_food(food_data: Food):
    try:
        food_dict = food_data.model_dump(mode="json", exclude_none=True)
        if "id" in food_dict:
            del food_dict["id"]
        if food_dict.get("merchant_id") == 0:
            food_dict["merchant_id"] = random.randint(2, 71)
            
        response = supabase.table("food").insert(food_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi thêm món ăn: {str(e)}")


# 4. UPDATE - Chỉ cho Merchant dùng (Đính kèm Depend)
# Cập nhật lại hàm PUT trong food_router.py
# Sửa lại hàm PUT trong food_router.py cho đúng thứ tự cú pháp .auth()
@router.put("/{food_id}", response_model=Food)
def update_food(
    food_id: int, 
    food_data: FoodUpdate, 
    merchant_id: str = Depends(verify_merchant_role) # <-- THÊM DÒNG NÀY ĐỂ CHECK QUYỀN
):  
    try:
        check_exist = supabase.table("food").select("id").eq("id", food_id).execute()
        if not check_exist.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Món ăn ID = {food_id} không tồn tại để cập nhật"
            )

        update_payload = food_data.model_dump(mode="json", exclude_none=True)
        print("DEBUG payload:", update_payload)  # log để kiểm tra
        response = supabase.table("food").update(update_payload).eq("id", food_id).select().execute()
        print("RAW row:", response.data)
        return response.data[0]
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Lỗi cập nhật món: {str(e)}")
    
# 5. DELETE - Chỉ cho Merchant dùng (Đính kèm Depend)
@router.delete("/{food_id}", status_code=status.HTTP_200_OK)
def delete_food(
    food_id: int, 
    merchant_id: str = Depends(verify_merchant_role) # <-- THÊM DÒNG NÀY ĐỂ CHECK QUYỀN
):
    try:
        check_exist = supabase.table("food").select("id").eq("id", food_id).execute()
        if not check_exist.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Món ăn ID = {food_id} không tồn tại để xóa"
            )

        supabase.table("food").delete().eq("id", food_id).execute()
        return {"message": f"Đã xóa thành công món ăn có ID = {food_id}"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))