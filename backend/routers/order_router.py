from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import Orders

router = APIRouter(prefix="/api/v1/orders", tags=["Orders CRUD"])

@router.get("/", response_model=List[Orders])
def get_all_orders():
    response = supabase.table("orders").select("*").execute()
    return response.data

@router.get("/{order_id}", response_model=Orders)
def get_order_by_id(order_id: int):
    response = supabase.table("orders").select("*").eq("id", order_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return response.data[0]

@router.post("/", response_model=Orders, status_code=201)
def create_order(order_data: Orders):
    data = order_data.model_dump(exclude_none=True)
    if "id" in data: del data["id"]
    response = supabase.table("orders").insert(data).execute()
    return response.data[0]


@router.delete("/{order_id}")
def delete_order(order_id: int):
    supabase.table("orders").delete().eq("id", order_id).execute()
    return {"message": f"Đã xóa đơn hàng {order_id}"}