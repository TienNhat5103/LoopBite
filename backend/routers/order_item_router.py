from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import OrderItems

router = APIRouter(prefix="/api/v1/order-items", tags=["Order Items CRUD"])

@router.get("/", response_model=List[OrderItems])
def get_all_order_items():
    response = supabase.table("order_items").select("*").execute()
    return response.data

@router.post("/", response_model=OrderItems, status_code=201)
def create_order_item(item_data: OrderItems):
    data = item_data.model_dump(exclude_none=True)
    if "id" in data: del data["id"]
    response = supabase.table("order_items").insert(data).execute()
    return response.data[0]

@router.delete("/{item_id}")
def delete_order_item(item_id: int):
    supabase.table("order_items").delete().eq("id", item_id).execute()
    return {"message": f"Đã xóa chi tiết đơn hàng {item_id}"}