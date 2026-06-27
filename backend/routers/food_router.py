from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import Food,FoodUpdate  # Import class Food và FoodUpdate từ folder models
import random  # Import thư viện random để sử dụng trong logic random merchant_id

router = APIRouter(
    prefix="/api/v1/food",
    tags=["Food CRUD Operations"]
)

# 1. READ ALL - Lấy toàn bộ danh sách món ăn (GET)
@router.get("/", response_model=List[Food])
def get_all_food():
    try:
        response = supabase.table("food").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Lỗi lấy danh sách món: {str(e)}"
        )

# 2. READ BY ID - Lấy chi tiết 1 món ăn bằng ID (GET)
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

# 3. CREATE - Nhập món ăn mới (POST)
@router.post("/", response_model=Food, status_code=201)
def create_food(food_data: Food):
    try:
        # 1. Chuyển đổi dữ liệu model sang định dạng json-safe dictionary
        food_dict = food_data.model_dump(mode="json", exclude_none=True)
        
        # 2. Xóa trường id ra khỏi payload để kích hoạt tự động tăng dưới DB
        if "id" in food_dict:
            del food_dict["id"]
            
        # 3. LOGIC RANDOM MERCHANT_ID: Nếu nhập vào bằng 0, bốc ngẫu nhiên từ 2 đến 71
        if food_dict.get("merchant_id") == 0:
            food_dict["merchant_id"] = random.randint(2, 71)
            
        # 4. Gửi dữ liệu xuống Supabase
        response = supabase.table("food").insert(food_dict).execute()
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Lỗi thêm món ăn: {str(e)}"
        )

# 4. UPDATE - Sửa đổi thông tin món ăn (PUT)
from models import Food, FoodUpdate  # <-- Nhớ import thêm FoodUpdate ở đầu file

@router.put("/{food_id}", response_model=Food)
def update_food(food_id: int, food_data: FoodUpdate):  # <-- Đổi ở đây thành FoodUpdate
    try:
        # 1. Kiểm tra xem món ăn có tồn tại không
        check_exist = supabase.table("food").select("id").eq("id", food_id).execute()
        if not check_exist.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Món ăn ID = {food_id} không tồn tại để cập nhật"
            )

        # 2. Dump data an toàn dưới dạng JSON (Lúc này mặc định chỉ có đúng price và quantity)
        update_payload = food_data.model_dump(mode="json", exclude_none=True)

        # 3. Tiến hành cập nhật lên Supabase
        response = supabase.table("food").update(update_payload).eq("id", food_id).execute()
        
        # Trả về bản ghi đầy đủ sau khi sửa
        return response.data[0]
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Lỗi cập nhật món: {str(e)}"
        )

# 5. DELETE - Xóa món ăn (DELETE)
@router.delete("/{food_id}", status_code=status.HTTP_200_OK)
def delete_food(food_id: int):
    try:
        # Kiểm tra tồn tại
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )