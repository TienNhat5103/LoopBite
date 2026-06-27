from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import Merchants

router = APIRouter(prefix="/api/v1/merchants", tags=["Merchants CRUD"])

@router.get("/", response_model=List[Merchants])
def get_all_merchants():
    response = supabase.table("merchants").select("*").execute()
    return response.data

@router.get("/{merchant_id}", response_model=Merchants)
def get_merchant_by_id(merchant_id: int):
    response = supabase.table("merchants").select("*").eq("id", merchant_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Không tìm thấy cửa hàng")
    return response.data[0]

@router.post("/", response_model=Merchants, status_code=201)
def create_merchant(merchant_data: Merchants):
    data = merchant_data.model_dump(exclude_none=True)
    if "id" in data: del data["id"]
    response = supabase.table("merchants").insert(data).execute()
    return response.data[0]

@router.put("/{merchant_id}", response_model=Merchants)
def update_merchant(merchant_id: int, merchant_data: Merchants):
    data = merchant_data.model_dump(exclude_none=True, exclude={"id"})
    response = supabase.table("merchants").update(data).eq("id", merchant_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Cửa hàng không tồn tại để cập nhật")
    return response.data[0]

@router.delete("/{merchant_id}")
def delete_merchant(merchant_id: int):
    response = supabase.table("merchants").delete().eq("id", merchant_id).execute()
    return {"message": f"Đã xóa cửa hàng {merchant_id}"}