from fastapi import APIRouter, HTTPException, status
from typing import List
from database import supabase
from models import Profiles, ProfileUpdate  # <-- Import ProfileUpdate từ models

router = APIRouter(prefix="/api/v1/profiles", tags=["Profiles CRUD"])

@router.get("/", response_model=List[Profiles])
def get_all_profiles():
    response = supabase.table("profiles").select("*").execute()
    return response.data


@router.put("/{profile_id}", response_model=Profiles)
def update_profile(profile_id: str, profile_data: ProfileUpdate): # <-- Đổi sang ProfileUpdate
    try:
        # 1. Chuyển đổi dữ liệu input sang dict dạng JSON-safe (chỉ chứa full_name và role)
        data = profile_data.model_dump(mode="json", exclude_none=True)
        
        if not data:
            raise HTTPException(status_code=400, detail="Không có dữ liệu hợp lệ để cập nhật")

        # 2. Tiến hành cập nhật lên Supabase dựa vào profile_id trên URL
        response = supabase.table("profiles").update(data).eq("id", profile_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại để cập nhật")
            
        return response.data[0]
        
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi cập nhật profile: {str(e)}")