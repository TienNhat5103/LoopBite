# 🍱 LoopBite — Project Workflows

> Tài liệu đặc tả luồng nghiệp vụ cho **User Flow** và **Merchant Flow** của hệ thống LoopBite.

---

## 📋 Mục lục

- [🍱 LoopBite — Project Workflows](#-loopbite--project-workflows)
  - [📋 Mục lục](#-mục-lục)
  - [1. User Flow — Luồng Người Dùng](#1-user-flow--luồng-người-dùng)
    - [1.1 Sơ đồ luồng](#11-sơ-đồ-luồng)
    - [1.2 Mô tả từng bước](#12-mô-tả-từng-bước)
    - [1.3 Demo Flow Example](#13-demo-flow-example)
  - [2. Merchant Flow — Luồng Cửa Hàng](#2-merchant-flow--luồng-cửa-hàng)
    - [2.1 Sơ đồ luồng](#21-sơ-đồ-luồng)
    - [2.2 Mô tả từng bước](#22-mô-tả-từng-bước)
    - [2.3 Điều kiện hiển thị món ăn](#23-điều-kiện-hiển-thị-món-ăn)
    - [2.4 High-Level Pipeline](#24-high-level-pipeline)

---

## 1. User Flow — Luồng Người Dùng

> Mô tả trải nghiệm của khách hàng từ khi mở ứng dụng, tìm kiếm đồ ăn giải cứu, cho đến khi nhận được mã xác nhận đơn hàng thành công.

### 1.1 Sơ đồ luồng

![User Flow Diagram](Userflow.png)

---

### 1.2 Mô tả từng bước

| # | Bước | Mô tả |
|---|------|--------|
| 1 | 🚀 **START — Mở LoopBite** | Người dùng mở ứng dụng LoopBite trên thiết bị di động. |
| 2 | 🔍 **Search & Location** | User nhập từ khóa tìm kiếm (vd: `bánh mì`, `bánh ngọt`, `snack`, `đồ ăn đêm`). Hệ thống yêu cầu truy cập vị trí GPS hiện tại. |
| 3 | 🗺️ **Browse Results** | Hệ thống hiển thị bản đồ và danh sách **Rescue Food** gần nhất dựa trên vị trí người dùng. |
| 4 | 🎛️ **Filter Results** | Người dùng lọc kết quả theo tiêu chí mong muốn. |
| 5 | 📄 **View Item Details** | Chọn món để xem chi tiết đầy đủ. |
| 6 | ✅ **Confirm Order & Choose Pickup** | Xác nhận đơn và chọn phương thức nhận hàng + thanh toán. |
| 7 | ⚙️ **Order Creation** | Hệ thống tự động tạo đơn, giữ số lượng và sinh mã QR. |
| 8 | 🎉 **END — Order Confirmation** | Người dùng nhận trang xác nhận đơn hàng thành công. |

---

**Bộ lọc khả dụng (Bước 4):**

| Bộ lọc | Mô tả |
|--------|-------|
| 🍜 Food Type | Loại thực phẩm |
| 📍 Distance | Khoảng cách |
| 💰 Price | Giá cả |
| 🕐 Pickup Time | Khung giờ lấy hàng |
| 📅 Best Before | Hạn sử dụng tốt nhất |
| 📦 Quantity Remaining | Số lượng còn lại |

**Thông tin chi tiết món ăn (Bước 5):**

| Trường | Mô tả |
|--------|-------|
| Name | Tên món |
| Shop Name | Tên cửa hàng |
| Food Type | Loại thực phẩm |
| Quantity Left | Số lượng còn lại |
| Pickup Time | Khung giờ lấy hàng |
| Best Before | Hạn sử dụng tốt nhất |

**Tùy chọn đặt hàng (Bước 6):**

| | Lựa chọn A | Lựa chọn B |
|-|-----------|-----------|
| 🚗 **Pickup Method** | Nhận tại cửa hàng | Giao hàng (Delivery) |
| 💳 **Payment Method** | Thanh toán tại quầy | Thanh toán trực tuyến |

**Thông tin xác nhận đơn hàng (Bước 8):**

| Trường | Nội dung |
|--------|----------|
| 🔑 Pickup Code | Mã nhận hàng |
| 🏪 Shop Name | Tên cửa hàng |
| 📍 Address | Địa chỉ |
| 🕐 Pickup Time | Khung giờ lấy hàng |
| 💰 Total Amount | Tổng tiền |
| 📋 Order Status | Trạng thái đơn hàng |

---

### 1.3 Demo Flow Example

```
🔍 Tìm kiếm "bánh ngọt"
    ↓
📍 Lấy vị trí — Xác định tọa độ người dùng
    ↓
🎛️ Lọc kết quả — Tìm tiệm bánh gần nhất (Nearest Bakery)
    ↓
🧁 Chọn món — Xem chi tiết và chọn sản phẩm
    ↓
📌 Đặt chỗ — Giữ chỗ món ăn (Reserve Item)
    ↓
✅ Hoàn tất — Nhận mã lấy hàng (Receive Pickup Code)
```

---

## 2. Merchant Flow — Luồng Cửa Hàng

> Mô tả quy trình của chủ cửa hàng từ khi đăng bán mặt hàng giải cứu, quản lý hiển thị, cho đến khi hoàn thành bàn giao đơn hàng cho khách.

### 2.1 Sơ đồ luồng

![Merchant Flow Diagram](MerchantFlow.png)

---

### 2.2 Mô tả từng bước

| # | Bước | Mô tả |
|---|------|--------|
| 1 | 🚀 **START — Mở Merchant App** | Đối tác mở ứng dụng dành riêng cho Merchant. |
| 2 | 📋 **Go to Listings** | Điều hướng vào trang **"Danh sách của tôi"** (My Listings). |
| 3 | ➕ **Tap Post Item** | Bấm nút **"Đăng mặt hàng giải cứu"** (Post rescue item). |
| 4 | 📝 **Fill Details** | Điền đầy đủ thông tin sản phẩm. |
| 5 | 📢 **Tap Publish** | Nhấn nút **"Đăng tải"** (Publish). |
| 6 | 🔎 **Item Visibility Check** | Hệ thống kiểm tra điều kiện hiển thị món. |
| 7 | 📬 **Order Received** | Đơn hàng mới xuất hiện trên màn hình Merchant khi có khách đặt. |
| 8 | 🤝 **Confirm Pickup** | Khách đến, người bán kiểm tra mã và xác nhận giao hàng. |
| 9 | ⚙️ **System Updates** | Hệ thống tự động cập nhật trạng thái và tồn kho. |
| 10 | ✅ **END — Order Complete** | Đơn hàng hoàn thành trên hệ thống. |

---

**Thông tin cần điền khi đăng món (Bước 4):**

| Trường | Mô tả | Bắt buộc |
|--------|-------|----------|
| Item Name | Tên mặt hàng | ✅ |
| Food Category | Danh mục thực phẩm | ✅ |
| Quantity | Số lượng | ✅ |
| Original Price | Giá gốc | ✅ |
| Pickup Start Time | Giờ bắt đầu lấy hàng | ✅ |
| Pickup End Time | Giờ kết thúc lấy hàng | ✅ |
| Best Before | Hạn sử dụng tốt nhất | ✅ |
| Quality Notes | Ghi chú chất lượng | ✅ |

---

### 2.3 Điều kiện hiển thị món ăn

Sau khi Merchant nhấn **Publish**, hệ thống kiểm tra toàn bộ các điều kiện sau trước khi hiển thị món lên app của User:

```
Status = Published  ✅
    AND
Quantity > 0        ✅
    AND
Within Pickup Time Window  ✅
    AND
Low-Risk Category   ✅
```

| Kết quả | Hành động hệ thống |
|---------|-------------------|
| ✅ **Tất cả điều kiện đạt** | Món được hiển thị công khai đến người dùng (Item Visible to Users) |
| ❌ **Một hoặc nhiều điều kiện không đạt** | Món bị ẩn hoặc bị gắn cờ cảnh báo (Item Hidden / Flagged) |

---

**Logic cập nhật tồn kho (Bước 9):**

```
Khách xác nhận lấy hàng
    ↓
Trạng thái đơn  →  "Đã lấy hàng" (Picked up)
    ↓
Quantity  -=  1
    ↓
Nếu Quantity = 0  →  Trạng thái món  →  "Hết hàng" (Sold out)
```

---

### 2.4 High-Level Pipeline

```
🏪 Merchant đăng món
    ↓
👤 User đặt giữ chỗ
    ↓
📬 Merchant thấy đơn hàng
    ↓
🤝 Merchant xác nhận giao dịch
    ↓
📉 Hệ thống giảm tồn kho
    ↓
✅ Đơn hàng hoàn thành
```

---
