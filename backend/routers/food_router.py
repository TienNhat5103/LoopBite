from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import Food  # Import class Food đã sửa từ folder models

router = APIRouter(
    prefix="/api/v1/food",
    tags=["Food CRUD Operations"]
)

# 1. READ ALL - Lấy toàn bộ danh sách món ăn (GET)
@router.get("/", response_model=List[Food])
def get_all_food():
    try:
        print()
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
        response = supabase.table("Food").select("*").eq("id", food_id).execute()
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
@router.post("/", response_model=Food, status_code=status.HTTP_201_CREATED)
def create_food(food_data: Food):
    try:
        # Chuyển đổi Model thành Dict, loại bỏ ID để Postgres tự tăng
        food_dict = food_data.model_dump(exclude_none=True)
        if "id" in food_dict:
            del food_dict["id"]
            
        response = supabase.table("Food").insert(food_dict).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Lỗi thêm món ăn: {str(e)}"
        )

# 4. UPDATE - Sửa đổi thông tin món ăn (PUT)
@router.put("/{food_id}", response_model=Food)
def update_food(food_id: int, food_data: Food):
    try:
        # Kiểm tra xem món đó có tồn tại không trước khi sửa
        check_exist = supabase.table("Food").select("id").eq("id", food_id).execute()
        if not check_exist.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Món ăn ID = {food_id} không tồn tại để cập nhật"
            )

        food_dict = food_data.model_dump(exclude_none=True, exclude={"id"})
        response = supabase.table("Food").update(food_dict).eq("id", food_id).execute()
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
        check_exist = supabase.table("Food").select("id").eq("id", food_id).execute()
        if not check_exist.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Món ăn ID = {food_id} không tồn tại để xóa"
            )

        supabase.table("Food").delete().eq("id", food_id).execute()
        return {"message": f"Đã xóa thành công món ăn có ID = {food_id}"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )