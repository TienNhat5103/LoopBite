import unicodedata
from math import atan2, cos, radians, sin, sqrt

from fastapi import APIRouter, HTTPException, Query, status

from database import supabase


router = APIRouter(prefix="/api/v1/search", tags=["Food Search"])


def haversine_km(lat1, lng1, lat2, lng2):
    earth_radius_km = 6371

    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value or "")
    without_accents = "".join(
        character for character in normalized if unicodedata.category(character) != "Mn"
    )
    return without_accents.replace("đ", "d").replace("Đ", "D").casefold().strip()


class SearchService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_top_nearest_merchants(self, user_lat, user_lng):
        res = self.supabase.table("merchants").select("*").execute()
        merchants = res.data or []

        nearby_merchants = []

        for merchant in merchants:
            latitude = merchant.get("latitude")
            longitude = merchant.get("longitude")

            if latitude is None or longitude is None:
                continue

            distance = haversine_km(
                float(user_lat),
                float(user_lng),
                float(latitude),
                float(longitude),
            )

            merchant_with_distance = dict(merchant)
            merchant_with_distance["distance_km"] = round(distance, 2)
            nearby_merchants.append(merchant_with_distance)

        nearby_merchants.sort(key=lambda merchant: merchant["distance_km"])

        return nearby_merchants[:10]

    def search_food_nearby(self, keyword, user_lat, user_lng):
        normalized_keyword = normalize_text(keyword)
        if not normalized_keyword:
            return []

        nearby_merchants = self.get_top_nearest_merchants(
            user_lat=user_lat,
            user_lng=user_lng,
        )

        if not nearby_merchants:
            return []

        merchant_ids = [merchant["id"] for merchant in nearby_merchants]

        food_res = (
            self.supabase.table("food")
            .select("*")
            .in_("merchant_id", merchant_ids)
            .execute()
        )
        foods = food_res.data or []

        foods_by_merchant_id = {}

        for item in foods:
            searchable_parts = [
                normalize_text(item.get("name", "")),
                normalize_text(item.get("category", "")),
            ]

            matches_keyword = any(
                normalized_keyword in part for part in searchable_parts if part
            )
            has_stock = (item.get("quantity") or 0) > 0
            is_active = str(item.get("status") or "").casefold() != "inactive"

            if not matches_keyword or not has_stock or not is_active:
                continue

            merchant_id = item["merchant_id"]
            foods_by_merchant_id.setdefault(merchant_id, []).append(item)

        results = []

        for merchant in nearby_merchants:
            matched_foods = foods_by_merchant_id.get(merchant["id"], [])
            if matched_foods:
                results.append(
                    {
                        "merchant": merchant,
                        "foods": matched_foods,
                    }
                )

        return results


search_service = SearchService(supabase)


@router.get("/foods")
def search_foods_nearby(
    keyword: str = Query(..., min_length=1, description="Ten mon an can tim"),
    user_lat: float = Query(..., description="Vi do cua nguoi dung"),
    user_lng: float = Query(..., description="Kinh do cua nguoi dung"),
):
    try:
        return {
            "keyword": keyword,
            "limit_store": 10,
            "results": search_service.search_food_nearby(
                keyword=keyword,
                user_lat=user_lat,
                user_lng=user_lng,
            ),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Loi khi tim kiem mon an: {exc}",
        ) from exc