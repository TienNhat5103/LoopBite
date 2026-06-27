"""
API client for FamilyMart Rescue backend.
Talks to FastAPI at http://127.0.0.1:8000
"""
import os
import requests
from typing import List, Optional, Dict, Any

API_BASE = os.environ.get("FAMILYMART_API", "http://127.0.0.1:8001")
TIMEOUT = 8


def _url(path: str) -> str:
    return f"{API_BASE}{path}"


def health() -> Dict[str, Any]:
    """Ping an actual API endpoint (backend has no / route)."""
    try:
        r = requests.get(_url("/api/v1/merchants/"), timeout=TIMEOUT)
        r.raise_for_status()
        return {"ok": True, "data": r.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------- MERCHANTS ----------
def list_merchants() -> List[Dict[str, Any]]:
    try:
        r = requests.get(_url("/api/v1/merchants/"), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json() or []
    except Exception as e:
        print(f"[api] list_merchants err: {e}")
        return []


def get_merchant(merchant_id: int) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(_url(f"/api/v1/merchants/{merchant_id}"), timeout=TIMEOUT)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[api] get_merchant err: {e}")
        return None


# ---------- FOOD ----------
def list_food(merchant_id: Optional[int] = None) -> List[Dict[str, Any]]:
    try:
        r = requests.get(_url("/api/v1/food/"), timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json() or []
        if merchant_id is not None:
            data = [f for f in data if f.get("merchant_id") == merchant_id]
        return data
    except Exception as e:
        print(f"[api] list_food err: {e}")
        return []


def _to_postgres_dt(iso_str: Optional[str]) -> Optional[str]:
    """Convert any datetime string to 'YYYY-MM-DDTHH:MM:SS+00:00' format
    that Pydantic can parse AND re-serialize for Supabase."""
    if not iso_str:
        return None
    try:
        from datetime import datetime, timezone
        s = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # Pydantic + supabase lib need ISO with colon in tz
        return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    except Exception:
        return iso_str


def create_food(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        if "expiry_time" in payload:
            payload = {**payload, "expiry_time": _to_postgres_dt(payload["expiry_time"])}
        r = requests.post(_url("/api/v1/food/"), json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[api] create_food err: {e} | payload={payload}")
        return None


def delete_food(food_id: int) -> bool:
    try:
        r = requests.delete(_url(f"/api/v1/food/{food_id}"), timeout=TIMEOUT)
        return r.status_code == 200
    except Exception as e:
        print(f"[api] delete_food err: {e}")
        return False


# ---------- SEARCH ----------
def search_foods(keyword: str, user_lat: float, user_lng: float) -> Dict[str, Any]:
    try:
        r = requests.get(
            _url("/api/v1/search/foods"),
            params={"keyword": keyword, "user_lat": user_lat, "user_lng": user_lng},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[api] search_foods err: {e}")
        return {"keyword": keyword, "limit_store": 0, "results": []}


# ---------- HELPERS ----------
def fmt_vnd(amount: float) -> str:
    """Format VND: 15000 -> '15,000đ'."""
    if amount is None:
        return "0đ"
    return f"{int(amount):,}".replace(",", ",") + "đ"


def fmt_vnd_short(amount: float) -> str:
    """Compact: 450000 -> '450K', 1500000 -> '1.5M'."""
    if amount is None:
        return "0"
    amount = int(amount)
    if amount >= 1_000_000:
        return f"{amount/1_000_000:.1f}M".rstrip("0").rstrip(".")
    if amount >= 1_000:
        return f"{int(amount/1_000)}K"
    return str(amount)


def category_emoji(category: str) -> str:
    if not category:
        return "🍱"
    cat = category.lower()
    if any(k in cat for k in ["onigiri", "cơm", "rice"]):
        return "🍙"
    if any(k in cat for k in ["sandwich", "bánh mì"]):
        return "🥪"
    if any(k in cat for k in ["bento", "cơm hộp"]):
        return "🍱"
    if any(k in cat for k in ["salad", "rau"]):
        return "🥗"
    if any(k in cat for k in ["bread", "bánh", "melon"]):
        return "🍞"
    if any(k in cat for k in ["drink", "nước", "trà", "tea", "coffee"]):
        return "🥤"
    if any(k in cat for k in ["chocolate"]):
        return "🍫"
    return "🍱"


def time_until(exp_str: Optional[str]) -> str:
    """Returns 'Xh left' or 'expired' from ISO datetime string."""
    if not exp_str:
        return "—"
    try:
        from datetime import datetime, timezone
        # Backend returns timezone-aware ISO like "2026-03-30T17:00:00Z"
        exp = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = exp - now
        secs = int(diff.total_seconds())
        if secs <= 0:
            return "expired"
        hours = secs // 3600
        if hours < 1:
            mins = secs // 60
            return f"{mins}m left"
        if hours < 24:
            return f"{hours}h left"
        days = hours // 24
        return f"{days}d left"
    except Exception:
        return "—"