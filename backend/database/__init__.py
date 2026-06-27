import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load các biến môi trường từ file .env vào hệ thống
load_dotenv()

# Đọc cấu hình từ os.environ
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Kiểm tra xem đã load thành công chưa để tránh crash app ngầm
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Lỗi: Thiếu SUPABASE_URL hoặc SUPABASE_KEY trong file .env")

# Khởi tạo Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)