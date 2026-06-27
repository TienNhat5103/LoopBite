from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from database import supabase
from models import Orders
from models.orders import OrderCreateRequest
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

        # 2. Tính toán tổng tiền (amount) tự động từ Database để chống client sửa giá
        total_amount = 0.0
        calculated_items = []
        
        for item in order_input.items:
            # Lấy thông tin giá từ bảng food
            food_res = supabase.table("food").select("price", "name").eq("id", item.food_id).execute()
            if not food_res.data:
                raise HTTPException(status_code=44, detail=f"Món ăn có ID = {item.food_id} không tồn tại")
            
            food_info = food_res.data[0]
            price = food_info.get("price", 0)
            item_total = float(price * item.quantity)
            total_amount += item_total
            
            # Lưu lại thông tin tạm thời để chèn vào bảng order_items sau
            calculated_items.append({
                "food_id": item.food_id,
                "quantity": item.quantity,
                "total_price": item_total
            })

        # 3. Tạo đơn hàng tổng (Bảng orders)
        order_payload = {
            "user_id": user_id,
            "amount": total_amount,
            "purchase_type": order_input.purchase_type,
            "status": "pending"  # Trạng thái mặc định ban đầu là chờ xử lý
        }
        
        # Gán token để thực hiện với quyền user hiện tại
        supabase.postgrest.auth(token)
        order_res = supabase.table("orders").insert(order_payload).execute()
        
        if not order_res.data:
            raise HTTPException(status_code=400, detail="Không thể khởi tạo đơn hàng")
        
        new_order = order_res.data[0]
        new_order_id = new_order.get("id") # Lấy ra ID đơn hàng tự động tăng vừa sinh

        # 4. Tạo chi tiết đơn hàng (Bảng order_items) bổ sung order_id vừa lấy được
        for calc_item in calculated_items:
            calc_item["order_id"] = new_order_id
            
        # Insert hàng loạt (Bulk Insert) danh sách chi tiết món xuống Supabase
        supabase.table("order_items").insert(calculated_items).execute()
        
        # Trả về kết quả sạch token
        supabase.postgrest.auth("")
        
        return {
            "message": "Đặt hàng thành công! 🎉",
            "order_id": new_order_id,
            "total_amount": total_amount,
            "status": "pending",
            "items_count": len(calculated_items)
        }

    except HTTPException as http_ex:
        supabase.postgrest.auth("")
        raise http_ex
    except Exception as e:
        supabase.postgrest.auth("")
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi đặt hàng: {str(e)}")

@router.delete("/{order_id}")
def delete_order(order_id: int):
    supabase.table("orders").delete().eq("id", order_id).execute()
    return {"message": f"Đã xóa đơn hàng {order_id}"}