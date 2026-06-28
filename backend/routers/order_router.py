from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from database import supabase,SUPABASE_KEY
from models import Orders
from models.orders import OrderCreateRequest, UpdateStatusRequest, CartItemInput
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/v1/orders", tags=["Orders CRUD"])
security = HTTPBearer()

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

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order_input: OrderCreateRequest, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    try:
        # 1. Xác thực Token để lấy user_id (UUID) của người mua
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        if not order_input.items:
            raise HTTPException(status_code=400, detail="Giỏ hàng không được để trống")

        # 2. Tính toán tổng tiền & Kiểm tra số lượng tồn kho
        total_amount = 0.0
        calculated_items = []
        stock_updates = []
        
        for item in order_input.items:
            food_res = supabase.table("food").select("price", "name", "quantity").eq("id", item.food_id).execute()
            if not food_res.data:
                raise HTTPException(status_code=404, detail=f"Món ăn có ID = {item.food_id} không tồn tại")
            
            food_info = food_res.data[0]
            current_stock = food_info.get("quantity", 0)
            
            if item.quantity > current_stock:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Món '{food_info.get('name')}' không đủ số lượng! (Còn lại: {current_stock}, Yêu cầu: {item.quantity})"
                )
            
            price = food_info.get("price", 0)
            item_total = float(price * item.quantity)
            total_amount += item_total
            
            calculated_items.append({
                "food_id": item.food_id,
                "quantity": item.quantity,
                "total_price": item_total
            })
            
            stock_updates.append({
                "food_id": item.food_id,
                "new_stock": current_stock - item.quantity
            })

        # 3. Tạo đơn hàng tổng
        order_payload = {
            "user_id": user_id,
            "amount": total_amount,
            "purchase_type": order_input.purchase_type,
            "status": "pending"
        }
        
        # Gán token để thực hiện với quyền User hiện tại
        supabase.postgrest.auth(token)
        order_res = supabase.table("orders").insert(order_payload).execute()
        
        if not order_res.data:
            raise HTTPException(status_code=400, detail="Không thể khởi tạo đơn hàng")
        
        new_order = order_res.data[0]
        new_order_id = new_order.get("id")

        # 4. Tạo chi tiết đơn hàng
        for calc_item in calculated_items:
            calc_item["order_id"] = new_order_id
            
        supabase.table("order_items").insert(calculated_items).execute()
        
        # 5. Khôi phục lại Anon Key (Thay vì truyền chuỗi rỗng "")
        supabase.postgrest.auth(SUPABASE_KEY) 
        
        # 6. Tiến hành trừ kho
        for stock_info in stock_updates:
            supabase.table("food").update({
                "quantity": stock_info["new_stock"]
            }).eq("id", stock_info["food_id"]).execute()
        
        return {
            "message": "Đặt hàng thành công",
            "order_id": new_order_id,
            "total_amount": total_amount,
            "status": "pending",
            "items_count": len(calculated_items)
        }

    except HTTPException as http_ex:
        supabase.postgrest.auth(SUPABASE_KEY) # <-- Trả lại Anon Key khi dính lỗi logic
        raise http_ex
    except Exception as e:
        supabase.postgrest.auth(SUPABASE_KEY) # <-- Trả lại Anon Key khi dính lỗi hệ thống
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi đặt hàng: {str(e)}")
    
@router.delete("/{order_id}")
def delete_order(order_id: int):
    supabase.table("orders").delete().eq("id", order_id).execute()
    return {"message": f"Đã xóa đơn hàng {order_id}"}

@router.put("/{order_id}/status")
def update_order_status(order_id: int, payload: UpdateStatusRequest):
    try:
        # Sử dụng Anon Key mặc định sạch (Không cần truyền Token Auth của User)
        supabase.postgrest.auth(SUPABASE_KEY)
        
        # 1. Kiểm tra đơn hàng có tồn tại hay không trước khi update
        check_order = supabase.table("orders").select("id").eq("id", order_id).execute()
        if not check_order.data:
            raise HTTPException(
                status_code=404, 
                detail=f"Đơn hàng có ID = {order_id} không tồn tại trên hệ thống"
            )
            
        # 2. Tiến hành cập nhật trạng thái mới
        response = (
            supabase
            .table("orders")
            .update({"status": payload.status})
            .eq("id", order_id)
            .execute()
        )
        
        return {
            "success": True,
            "message": f"Cập nhật trạng thái đơn hàng {order_id} thành '{payload.status}' thành công! 🚀",
            "updated_data": response.data[0]
        }
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Lỗi hệ thống khi cập nhật trạng thái đơn: {str(e)}"
        )