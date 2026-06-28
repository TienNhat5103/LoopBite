# Tài liệu API

## Nhóm 1: Authentication (Xác thực tài khoản)

---

### 1. Đăng ký tài khoản mới

**Endpoint:** `POST /api/v1/auth/register`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "Nguyễn Văn A"
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `email` | String | ✅ | Email đăng ký |
| `password` | String | ✅ | Mật khẩu |
| `full_name` | String | ✅ | Họ và tên |

**Responses:**

`201 Created`
```json
{
  "message": "Đăng ký thành công! Vui lòng kiểm tra email để xác thực (nếu có bật)",
  "user_id": "d3b07384-d113-4956-a5d6-ec2e31713506"
}
```

`400 Bad Request` — Email đã tồn tại hoặc lỗi cú pháp
```json
{
  "detail": "Lỗi đăng ký: <chi tiết lỗi hệ thống>"
}
```

---

### 2. Đăng nhập (Lấy Access Token)

**Endpoint:** `POST /api/v1/auth/login`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `email` | String | ✅ | Email tài khoản |
| `password` | String | ✅ | Mật khẩu |

**Responses:**

`200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "user": {
    "id": "d3b07384-d113-4956-a5d6-ec2e31713506",
    "email": "user@example.com"
  }
}
```

`400 Bad Request` — Sai tài khoản hoặc mật khẩu
```json
{
  "detail": "Sai tài khoản hoặc mật khẩu: <chi tiết lỗi>"
}
```

---

### 3. Lấy thông tin tài khoản hiện tại

**Endpoint:** `GET /api/v1/auth/me`

**Headers:**

| Key | Value |
|-----|-------|
| Authorization | Bearer `<access_token>` |

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
{
  "auth_id": "d3b07384-d113-4956-a5d6-ec2e31713506",
  "profile_details": {
    "id": "d3b07384-d113-4956-a5d6-ec2e31713506",
    "full_name": "Nguyễn Văn A",
    "role": "user"
  }
}
```

`401 Unauthorized` — Token không hợp lệ hoặc hết hạn
```json
{
  "detail": "Token không hợp lệ hoặc đã hết hạn: <chi tiết lỗi>"
}
```

`404 Not Found` — Không tìm thấy thông tin profile tương ứng
```json
{
  "detail": "Không tìm thấy profile tương ứng với User ID này"
}
```

---

### 4. Xóa tài khoản người dùng

**Endpoint:** `DELETE /api/v1/auth/delete-user/{user_id}`

**Headers:** Không yêu cầu (sử dụng quyền Admin ngầm định trên server).

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
{
  "status": "Thành công",
  "message": "Tài khoản có ID {user_id} đã bị xóa hoàn toàn khỏi auth.users và public.profiles."
}
```

`400 Bad Request` — Lỗi khi xóa tài khoản
```json
{
  "detail": "Lỗi khi xóa tài khoản có ID {user_id}: <chi tiết lỗi>"
}
```

---

## Nhóm 2: Profiles CRUD (Quản lý thông tin người dùng)

---

### 1. Lấy danh sách tất cả Profiles

**Endpoint:** `GET /api/v1/profiles/`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
[
  {
    "id": "d3b07384-d113-4956-a5d6-ec2e31713506",
    "full_name": "Nguyễn Văn A",
    "role": "user"
  }
]
```

---

### 2. Cập nhật thông tin Profile

**Endpoint:** `PUT /api/v1/profiles/{profile_id}`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "full_name": "Nguyễn Văn B",
  "role": "merchant"
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `full_name` | String | ❌ | Họ và tên mới |
| `role` | String | ❌ | Vai trò mới |

**Responses:**

`200 OK`
```json
{
  "id": "d3b07384-d113-4956-a5d6-ec2e31713506",
  "full_name": "Nguyễn Văn B",
  "role": "merchant"
}
```

`400 Bad Request` — Không truyền dữ liệu hợp lệ hoặc lỗi cập nhật
```json
{
  "detail": "Không có dữ liệu hợp lệ để cập nhật"
}
```

`404 Not Found` — Không tìm thấy ID người dùng
```json
{
  "detail": "Người dùng không tồn tại để cập nhật"
}
```

---

## Nhóm 3: Merchants CRUD (Quản lý cửa hàng)

---

### 1. Lấy danh sách tất cả cửa hàng

**Endpoint:** `GET /api/v1/merchants/`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
[
  {
    "id": 1,
    "name": "Bún Chả Hà Nội",
    "address": "123 Đường ABC",
    "latitude": 21.0285,
    "longitude": 105.8542
  }
]
```

---

### 2. Lấy thông tin chi tiết một cửa hàng

**Endpoint:** `GET /api/v1/merchants/{merchant_id}`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
{
  "id": 1,
  "name": "Bún Chả Hà Nội",
  "address": "123 Đường ABC",
  "latitude": 21.0285,
  "longitude": 105.8542
}
```

`404 Not Found`
```json
{
  "detail": "Không tìm thấy cửa hàng"
}
```

---

### 3. Lấy danh sách món ăn theo cửa hàng

**Endpoint:** `GET /api/v1/merchants/merchant_food/{merchant_id}`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK` — Trả về mảng rỗng `[]` nếu quán chưa có món ăn nào
```json
[
  {
    "id": 10,
    "merchant_id": 1,
    "name": "Bún chả đặc biệt",
    "price": 50000.0,
    "quantity": 20,
    "status": "active"
  }
]
```

`500 Internal Server Error`
```json
{
  "detail": "Lỗi lấy danh sách món theo cửa hàng: <chi tiết lỗi>"
}
```

---

### 4. Tạo mới một cửa hàng

**Endpoint:** `POST /api/v1/merchants/`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):** Đối tượng Merchants đầy đủ thông tin. Hệ thống tự động bỏ qua trường `id` nếu truyền lên.

**Responses:**

`201 Created`
```json
{
  "id": 2,
  "name": "Cơm Tấm Sài Gòn",
  "address": "456 Đường XYZ",
  "latitude": 10.7626,
  "longitude": 106.6601
}
```

---

### 5. Cập nhật thông tin cửa hàng

**Endpoint:** `PUT /api/v1/merchants/{merchant_id}`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):** Thông tin chỉnh sửa của cửa hàng.

**Responses:**

`200 OK` — Dữ liệu cửa hàng sau khi cập nhật thành công.

`404 Not Found`
```json
{
  "detail": "Cửa hàng không tồn tại để cập nhật"
}
```

---

### 6. Xóa một cửa hàng

**Endpoint:** `DELETE /api/v1/merchants/{merchant_id}`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK`
```json
{
  "message": "Đã xóa cửa hàng 1"
}
```

---

## Nhóm 4: Food CRUD Operations (Quản lý món ăn)

---

### 1. Lấy tất cả món ăn

**Endpoint:** `GET /api/v1/food/`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK` — Danh sách tất cả món ăn sắp xếp theo ID tăng dần.

`500 Internal Server Error`
```json
{
  "detail": "Lỗi lấy danh sách món: <chi tiết lỗi>"
}
```

---

### 2. Lấy thông tin chi tiết một món ăn

**Endpoint:** `GET /api/v1/food/{food_id}`

**Headers:** Không có.

**Request Body:** Không có.

**Responses:**

`200 OK` — Chi tiết món ăn cần tìm.

`404 Not Found`
```json
{
  "detail": "Không tìm thấy món ăn có ID = 10"
}
```

`500 Internal Server Error`
```json
{
  "detail": "<chi tiết lỗi>"
}
```

---

### 3. Tạo món ăn mới

**Endpoint:** `POST /api/v1/food/`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):** Schema Food. Nếu `merchant_id` truyền vào bằng `0`, hệ thống tự chọn random ngẫu nhiên từ 2 đến 71.

**Responses:**

`201 Created` — Dữ liệu món ăn vừa khởi tạo.

`400 Bad Request`
```json
{
  "detail": "Lỗi thêm món ăn: <chi tiết lỗi>"
}
```

---

### 4. Cập nhật giá và số lượng món ăn

**Endpoint:** `PUT /api/v1/food/{food_id}`

**Headers:**

| Key | Value |
|-----|-------|
| Authorization | Bearer `<access_token>` — Yêu cầu Token thuộc quyền merchant |
| Content-Type | application/json |

**Request Body (JSON):** `FoodUpdate` — chứa các thông tin cần chỉnh sửa như `price`, `quantity`, v.v.

**Responses:**

`200 OK` — Dữ liệu món ăn sau khi sửa đổi.

`403 Forbidden` — Tài khoản không có quyền merchant
```json
{
  "detail": "Quyền truy cập bị từ chối! Chỉ tài khoản chủ cửa hàng (merchant) mới có quyền thực hiện hành động này."
}
```

`404 Not Found`
```json
{
  "detail": "Món ăn ID = 10 không tồn tại để cập nhật"
}
```

`400 Bad Request / 401 Unauthorized` — Lỗi xác thực token hoặc lỗi payload dữ liệu.

---

### 5. Xóa một món ăn

**Endpoint:** `DELETE /api/v1/food/{food_id}`

**Headers:**

| Key | Value |
|-----|-------|
| Authorization | Bearer `<access_token>` — Yêu cầu Token thuộc quyền merchant |

**Responses:**

`200 OK`
```json
{
  "message": "Đã xóa thành công món ăn có ID = 10"
}
```

`404 Not Found`
```json
{
  "detail": "Món ăn ID = 10 không tồn tại để xóa"
}
```

---

## Nhóm 5: Orders CRUD (Quản lý đơn hàng)

---

### 1. Lấy danh sách tất cả các đơn hàng

**Endpoint:** `GET /api/v1/orders/`

**Headers:** Không có.

**Responses:**

`200 OK` — Mảng chứa toàn bộ dữ liệu đơn hàng tổng quan hệ thống.

---

### 2. Lấy thông tin chi tiết một đơn hàng

**Endpoint:** `GET /api/v1/orders/{order_id}`

**Responses:**

`200 OK` — Trả về đối tượng đơn hàng tổng quan theo ID.

`404 Not Found`
```json
{
  "detail": "Không tìm thấy đơn hàng"
}
```

---

### 3. Tạo đơn hàng mới (Đặt hàng)

**Endpoint:** `POST /api/v1/orders/`

**Headers:**

| Key | Value |
|-----|-------|
| Authorization | Bearer `<access_token>` — Tự động bóc tách để lấy ID người mua |
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "purchase_type": "delivery",
  "items": [
    {
      "food_id": 10,
      "quantity": 2
    }
  ]
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `purchase_type` | String | ✅ | Hình thức mua hàng |
| `items` | Array | ✅ | Danh sách món ăn đặt |
| `items[].food_id` | Integer | ✅ | ID món ăn |
| `items[].quantity` | Integer | ✅ | Số lượng |

**Responses:**

`201 Created`
```json
{
  "message": "Đặt hàng thành công",
  "order_id": 100,
  "total_amount": 100000.0,
  "status": "pending",
  "items_count": 1
}
```

`400 Bad Request` — Giỏ hàng trống hoặc món ăn không đủ số lượng tồn kho
```json
{
  "detail": "Món 'Bún chả đặc biệt' không đủ số lượng! (Còn lại: 1, Yêu cầu: 2)"
}
```

`404 Not Found`
```json
{
  "detail": "Món ăn có ID = 10 không tồn tại"
}
```

`500 Internal Server Error`
```json
{
  "detail": "Lỗi hệ thống khi đặt hàng: <chi tiết>"
}
```

---

### 4. Cập nhật trạng thái đơn hàng

**Endpoint:** `PUT /api/v1/orders/{order_id}/status`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "status": "completed"
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `status` | String | ✅ | Trạng thái đơn hàng cần cập nhật |

**Responses:**

`200 OK`
```json
{
  "success": true,
  "message": "Cập nhật trạng thái đơn hàng 100 thành 'completed' thành công! 🚀",
  "updated_data": {
    "id": 100,
    "status": "completed",
    "amount": 100000.0
  }
}
```

`404 Not Found`
```json
{
  "detail": "Đơn hàng có ID = 100 không tồn tại trên hệ thống"
}
```

---

### 5. Xóa đơn hàng

**Endpoint:** `DELETE /api/v1/orders/{order_id}`

**Responses:**

`200 OK`
```json
{
  "message": "Đã xóa đơn hàng 100"
}
```

---

## Nhóm 6: Order Items CRUD (Chi tiết món ăn trong đơn)

---

### 1. Lấy danh sách tất cả chi tiết món ăn

**Endpoint:** `GET /api/v1/order-items/`

**Responses:**

`200 OK` — Mảng dữ liệu tất cả các dòng chi tiết hóa đơn.

---

### 2. Tạo thủ công một dòng chi tiết món ăn

**Endpoint:** `POST /api/v1/order-items/`

**Headers:**

| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Request Body (JSON):**

```json
{
  "order_id": 100,
  "food_id": 10,
  "quantity": 2,
  "total_price": 100000.0
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| `order_id` | Integer | ✅ | ID đơn hàng |
| `food_id` | Integer | ✅ | ID món ăn |
| `quantity` | Integer | ✅ | Số lượng |
| `total_price` | Float | ✅ | Tổng giá trị |

**Responses:**

`201 Created` — Trả về đối tượng vừa tạo thành công từ database.

---

### 3. Xóa một dòng chi tiết món ăn

**Endpoint:** `DELETE /api/v1/order-items/{item_id}`

**Responses:**

`200 OK`
```json
{
  "message": "Đã xóa chi tiết đơn hàng 5"
}
```

---

## Nhóm 7: Food Search (Tìm kiếm món ăn xung quanh)

---

### 1. Tìm kiếm món ăn theo vị trí người dùng

**Endpoint:** `GET /api/v1/search/foods`

**Query Parameters:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `keyword` | String | ✅ | Từ khóa tên món hoặc danh mục cần tìm (không phân biệt dấu Tiếng Việt) |
| `user_lat` | Float | ✅ | Vĩ độ hiện tại của người dùng |
| `user_lng` | Float | ✅ | Kinh độ hiện tại của người dùng |

**Responses:**

`200 OK` — Tự động lọc top 10 quán gần nhất bằng công thức Haversine, chỉ hiển thị món còn hàng và đang active.

```json
{
  "keyword": "bun cha",
  "limit_store": 10,
  "results": [
    {
      "merchant": {
        "id": 1,
        "name": "Bún Chả Hà Nội",
        "latitude": 21.0285,
        "longitude": 105.8542,
        "distance_km": 1.45
      },
      "foods": [
        {
          "id": 10,
          "merchant_id": 1,
          "name": "Bún chả đặc biệt",
          "category": "Món nước",
          "price": 50000.0,
          "quantity": 20,
          "status": "active"
        }
      ]
    }
  ]
}
```

`500 Internal Server Error`
```json
{
  "detail": "Loi khi tim kiem mon an: <chi tiết lỗi hệ thống>"
}
```