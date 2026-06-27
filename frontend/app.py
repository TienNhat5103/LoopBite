"""
LoopBite MVP - Streamlit demo for users and merchants.
"""
import streamlit as st
from datetime import datetime, timedelta
import random

# ============================================================
# API CLIENT (talks to FastAPI at http://127.0.0.1:8000)
# ============================================================
import api_client as api

# Demo merchant - FamilyMart District 1 (id=17 from Supabase data)
DEMO_MERCHANT_ID = 17
API_OK = api.health().get("ok", False)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_food(merchant_id: int):
    return api.list_food(merchant_id=merchant_id)


@st.cache_data(ttl=30, show_spinner=False)
def _cached_merchants():
    return api.list_merchants()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="LoopBite",
    page_icon="LB",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM CSS - MOBILE FIRST
# ============================================================
st.markdown(
    """
<style>
/* Mobile-first container */
.main .block-container {
    max-width: 480px;
    padding: 1rem 1rem 6rem 1rem;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Primary color (green like FamilyMart) */
:root {
    --primary: #00A040;
    --primary-dark: #007A2F;
    --primary-light: #E6F7EE;
    --danger: #E63946;
    --warning: #F4A261;
    --text-dark: #1A1A1A;
    --text-gray: #6B7280;
    --bg-light: #F9FAFB;
    --border: #E5E7EB;
}

/* Card */
.food-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border: 1px solid var(--border);
}

/* Top bar */
.top-bar {
    background: var(--primary);
    color: white;
    padding: 1rem;
    border-radius: 0 0 16px 16px;
    margin: -1rem -1rem 1rem -1rem;
}

/* Status badge */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-active { background: var(--primary-light); color: var(--primary-dark); }
.badge-warn { background: #FFF3CD; color: #856404; }
.badge-danger { background: #F8D7DA; color: #721C24; }
.badge-gray { background: #E5E7EB; color: #374151; }

/* Bottom nav */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid var(--border);
    padding: 0.5rem 0;
    z-index: 999;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 2.75rem;
    font-weight: 600;
}

/* Hide default sidebar nav */
section[data-testid="stSidebarNav"] {display: none;}
/* MVP mode switch */
.mode-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem;
    margin-bottom: 1rem;
}
.mode-label {
    font-size: 0.78rem;
    color: var(--text-gray);
    font-weight: 700;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* User home */
.user-hero {
    background: linear-gradient(135deg, #0F8A4B 0%, #1FBF75 52%, #F6C85F 100%);
    color: #FFFFFF;
    padding: 1.15rem;
    border-radius: 0 0 18px 18px;
    margin: -1rem -1rem 1rem -1rem;
}
.user-hero h1 {
    margin: 0;
    font-size: 2rem;
    line-height: 1.05;
    letter-spacing: 0;
}
.user-hero p {
    margin: 0.5rem 0 0 0;
    color: rgba(255,255,255,0.9);
    font-size: 0.95rem;
}
.search-panel {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.location-ready {
    background: #E6F7EE;
    border: 1px solid #BFEBD1;
    color: #075C2D;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 0.88rem;
    margin: 0.5rem 0 0.75rem 0;
}
.location-missing {
    background: #FFF7E0;
    border: 1px solid #F6D58A;
    color: #6B4B00;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 0.88rem;
    margin: 0.5rem 0 0.75rem 0;
}
.demo-note {
    color: var(--text-gray);
    font-size: 0.82rem;
    margin-top: 0.4rem;
}
.map-panel {
    background: #102A1E;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    min-height: 8rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
}
.map-panel::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(31,191,117,0.28), rgba(246,200,95,0.22));
}
.map-panel > * {
    position: relative;
    z-index: 1;
}
.filter-bar {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem;
    margin-bottom: 0.9rem;
}
.result-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.result-title {
    font-weight: 800;
    color: var(--text-dark);
    font-size: 1.05rem;
}
.result-meta {
    color: var(--text-gray);
    font-size: 0.82rem;
    margin-top: 0.2rem;
}
.price-row {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-top: 0.55rem;
}
.rescue-price {
    color: var(--primary-dark);
    font-size: 1.12rem;
    font-weight: 800;
}
.original-price {
    color: #9CA3AF;
    font-size: 0.82rem;
    text-decoration: line-through;
}
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.45rem;
    margin-top: 0.75rem;
}
.info-pill {
    background: #F9FAFB;
    border: 1px solid #EEF2F7;
    border-radius: 9px;
    padding: 0.5rem;
    font-size: 0.78rem;
    color: #374151;
}
.detail-photo {
    min-height: 10rem;
    border-radius: 12px;
    background: linear-gradient(135deg, #E6F7EE 0%, #FFF7E0 100%);
    color: #007A2F;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 0.85rem;
}
.note-box {
    background: #FFFDF5;
    border: 1px solid #F6D58A;
    border-radius: 10px;
    padding: 0.75rem;
    color: #4B3A08;
    font-size: 0.88rem;
    margin-top: 0.75rem;
}
.review-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid #EEF2F7;
    font-size: 0.92rem;
}
.review-row:last-child {
    border-bottom: 0;
}
.review-label {
    color: var(--text-gray);
}
.review-value {
    color: var(--text-dark);
    font-weight: 700;
    text-align: right;
}
.pickup-code {
    background: #102A1E;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    margin-bottom: 0.85rem;
}
.pickup-code-value {
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}
.reservation-card {
    background: #FFFFFF;
    border: 1px solid #BFEBD1;
    border-left: 5px solid var(--primary);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.empty-state {
    background: #F9FAFB;
    border: 1px dashed #CBD5E1;
    border-radius: 12px;
    padding: 1rem;
    color: #475569;
    font-size: 0.9rem;
    margin-bottom: 0.85rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================
if "mode" not in st.session_state:
    st.session_state.mode = "User App"
if "page" not in st.session_state:
    st.session_state.page = "UserHome"
if "user_search_query" not in st.session_state:
    st.session_state.user_search_query = "pastry"
if "location_allowed" not in st.session_state:
    st.session_state.location_allowed = False
if "user_lat" not in st.session_state:
    st.session_state.user_lat = 10.7769
if "user_lng" not in st.session_state:
    st.session_state.user_lng = 106.7009
if "selected_food" not in st.session_state:
    st.session_state.selected_food = None
if "selected_quantity" not in st.session_state:
    st.session_state.selected_quantity = 1
if "pickup_method" not in st.session_state:
    st.session_state.pickup_method = "Pick up at store"
if "payment_method" not in st.session_state:
    st.session_state.payment_method = "Pay at counter"
if "active_reservation" not in st.session_state:
    st.session_state.active_reservation = None
if "mock_listings" not in st.session_state:
    st.session_state.mock_listings = []
if "quantity_overrides" not in st.session_state:
    st.session_state.quantity_overrides = {}


def navigate(page_name: str):
    """Change current page."""
    st.session_state.page = page_name
    st.rerun()


def set_mode(mode_name: str):
    """Switch between the user demo and merchant portal."""
    st.session_state.mode = mode_name
    st.session_state.page = "UserHome" if mode_name == "User App" else "Dashboard"
    st.rerun()


def set_user_search_query(term: str):
    """Set the search field from a quick-search button."""
    st.session_state.user_search_query = term

def vnd(amount):
    """Display VND without relying on special currency glyphs."""
    try:
        return f"{int(float(amount)):,} VND"
    except (TypeError, ValueError):
        return "0 VND"


def category_icon(category):
    cat = (category or "").lower()
    if any(word in cat for word in ["pastry", "bread", "bakery", "croissant"]):
        return "BA"
    if any(word in cat for word in ["noodle", "meal", "bento", "rice"]):
        return "ME"
    if any(word in cat for word in ["snack", "sweet"]):
        return "SN"
    return "FD"


def demo_results(keyword):
    """Reliable fallback data for the hackathon demo."""
    base = [
        {
            "id": "mock-pastry-1",
            "name": "Butter Croissant Rescue Box",
            "category": "Pastry",
            "store_name": "Sunrise Bakery",
            "store_address": "18 Le Loi, District 1",
            "distance_km": 0.6,
            "price": 18000,
            "original_price": 42000,
            "quantity": 5,
            "pickup_window": "Today 20:00-21:30",
            "best_before": "Best before 22:30",
            "quality_note": "Baked this morning, packed after display period.",
            "source": "mock",
        },
        {
            "id": "mock-bread-1",
            "name": "Assorted Bread Bag",
            "category": "Bread",
            "store_name": "FamilyMart District 1",
            "store_address": "20 Le Thanh Ton, District 1",
            "distance_km": 0.9,
            "price": 22000,
            "original_price": 50000,
            "quantity": 3,
            "pickup_window": "Today 21:00-22:00",
            "best_before": "Best before tonight",
            "quality_note": "Sealed packaged bread, still within best-before window.",
            "source": "mock",
        },
        {
            "id": "mock-snack-1",
            "name": "Late-night Snack Bundle",
            "category": "Snacks",
            "store_name": "Mini Stop Nguyen Hue",
            "store_address": "45 Nguyen Hue, District 1",
            "distance_km": 1.4,
            "price": 15000,
            "original_price": 33000,
            "quantity": 7,
            "pickup_window": "Today 22:00-23:30",
            "best_before": "Best before tomorrow",
            "quality_note": "Low-risk packaged items selected for quick pickup.",
            "source": "mock",
        },
    ]
    needle = (keyword or "").lower().strip()
    if not needle or needle == "pastry":
        return base
    matches = [item for item in base if needle in item["name"].lower() or needle in item["category"].lower()]
    return matches or base


def flatten_search_results(search_response, keyword):
    """Convert backend grouped search response into card-friendly rows."""
    rows = []
    for group in (search_response or {}).get("results", []):
        merchant = group.get("merchant") or {}
        for food in group.get("foods") or []:
            price = food.get("price") or 0
            rows.append(
                {
                    "id": food.get("id") or f"api-{len(rows)}",
                    "name": food.get("name", "Rescue food item"),
                    "category": food.get("category") or "Rescue Food",
                    "store_name": merchant.get("name") or "Nearby merchant",
                    "store_address": merchant.get("address") or "District 1 pickup point",
                    "distance_km": float(merchant.get("distance_km") or 1.0),
                    "price": price,
                    "original_price": int(float(price or 0) * 1.8) if price else 0,
                    "quantity": food.get("quantity") or 1,
                    "pickup_window": "Today 20:00-22:00",
                    "best_before": api.time_until(food.get("expiry_time")) if food.get("expiry_time") else "Best before tonight",
                    "quality_note": "Merchant-confirmed rescue item available for pickup.",
                    "source": "api",
                }
            )
    if keyword.lower().strip() == "pastry" and not any("pastry" in item["category"].lower() or "pastry" in item["name"].lower() or "croissant" in item["name"].lower() for item in rows):
        rows = demo_results(keyword) + rows
    return rows or demo_results(keyword)


def load_nearby_results(keyword):
    response = api.search_foods(keyword, st.session_state.user_lat, st.session_state.user_lng)
    return flatten_search_results(response, keyword)


def choose_food(item):
    st.session_state.selected_food = item
    st.session_state.selected_quantity = 1
    st.session_state.pickup_method = "Pick up at store"
    st.session_state.payment_method = "Pay at counter"
    navigate("FoodDetail")


def make_pickup_code():
    return f"LB-{random.randint(1000, 9999)}"


def apply_quantity_override(item):
    item_id = str(item.get("id"))
    if item_id in st.session_state.quantity_overrides:
        updated = dict(item)
        updated["quantity"] = st.session_state.quantity_overrides[item_id]
        return updated
    return item


def merchant_food_items():
    foods = _cached_food(DEMO_MERCHANT_ID) if API_OK else []
    combined = list(foods) + list(st.session_state.mock_listings)
    return [apply_quantity_override(food) for food in combined]


def add_mock_listing(payload, original_price=None, pickup_window=None, quality_note=None):
    listing = dict(payload)
    listing["id"] = f"mock-merchant-{len(st.session_state.mock_listings) + 1}"
    listing["original_price"] = original_price or int(float(payload.get("price") or 0) * 1.8)
    listing["pickup_window"] = pickup_window or "Today 20:00-22:00"
    listing["quality_note"] = quality_note or "Merchant-confirmed rescue item for same-day pickup."
    listing["source"] = "mock"
    st.session_state.mock_listings.append(listing)
    return listing


def confirm_pickup():
    reservation = st.session_state.active_reservation
    if not reservation:
        return
    item = dict(reservation["item"])
    item_id = str(item.get("id"))
    current_qty = int(st.session_state.quantity_overrides.get(item_id, item.get("quantity") or 0))
    new_qty = max(0, current_qty - int(reservation.get("quantity") or 1))
    st.session_state.quantity_overrides[item_id] = new_qty
    item["quantity"] = new_qty
    reservation["item"] = item
    reservation["status"] = "Picked Up"
    st.session_state.active_reservation = reservation
    if st.session_state.selected_food and str(st.session_state.selected_food.get("id")) == item_id:
        st.session_state.selected_food = item

def render_mode_switch():
    st.markdown(
        """
<div class="mode-card">
    <div class="mode-label">Demo mode</div>
</div>
""",
        unsafe_allow_html=True,
    )
    user_col, merchant_col = st.columns(2)
    with user_col:
        user_label = "User App active" if st.session_state.mode == "User App" else "User App"
        if st.button(user_label, key="mode_user", use_container_width=True):
            set_mode("User App")
    with merchant_col:
        merchant_label = "Merchant active" if st.session_state.mode == "Merchant Portal" else "Merchant Portal"
        if st.button(merchant_label, key="mode_merchant", use_container_width=True):
            set_mode("Merchant Portal")


# ============================================================
# PAGE: USER HOME / SEARCH
# ============================================================
def page_user_home():
    st.markdown(
        """
<div class="user-hero">
    <div style="font-size:0.8rem; font-weight:700; opacity:0.9; text-transform:uppercase; letter-spacing:0.04em;">LoopBite</div>
    <h1>Find rescue food nearby</h1>
    <p>Affordable food before it goes to waste. Built for students, late-night eaters, and anyone watching their budget.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.markdown("### What are you craving?")
    st.text_input(
        "Search food",
        key="user_search_query",
        placeholder="Try pastry, bread, noodles, snacks...",
        label_visibility="collapsed",
    )

    st.markdown("Quick searches")
    quick_terms = ["bread", "pastry", "noodles", "snacks", "late-night food"]
    quick_cols = st.columns(3)
    for index, term in enumerate(quick_terms):
        with quick_cols[index % 3]:
            st.button(
                term.title(),
                key=f"quick_{term}",
                use_container_width=True,
                on_click=set_user_search_query,
                args=(term,),
            )

    st.markdown("### Location")
    if st.session_state.location_allowed:
        st.markdown(
            """
<div class="location-ready">
    Demo location is ready: District 1, Ho Chi Minh City.
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<div class="location-missing">
    Use a demo location to find nearby rescue food.
</div>
""",
            unsafe_allow_html=True,
        )

    if st.button("Use my demo location", key="allow_location", use_container_width=True):
        st.session_state.location_allowed = True
        st.session_state.user_lat = 10.7769
        st.session_state.user_lng = 106.7009
        st.rerun()

    query = st.session_state.user_search_query.strip()
    if st.button("Search nearby food", key="search_nearby", type="primary", use_container_width=True):
        if not query:
            st.warning("Enter a food keyword first.")
        elif not st.session_state.location_allowed:
            st.warning("Use the demo location first so LoopBite can sort nearby food.")
        else:
            navigate("UserResults")

    st.markdown('<div class="demo-note">MVP demo tip: use Pastry to follow the short flow from search to pickup code.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: USER RESULTS
# ============================================================
def page_user_results():
    keyword = st.session_state.user_search_query.strip() or "pastry"
    results = [apply_quantity_override(item) for item in load_nearby_results(keyword)]

    st.markdown(
        f"""
<div class="user-hero">
    <div style="font-size:0.8rem; font-weight:700; opacity:0.9; text-transform:uppercase; letter-spacing:0.04em;">LoopBite</div>
    <h1>Nearby rescue food</h1>
    <p>Showing affordable {keyword.title()} options near District 1.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="map-panel">
    <div>
        <div style="font-size:0.78rem; opacity:0.82; font-weight:700; text-transform:uppercase;">Demo map area</div>
        <div style="font-size:1.15rem; font-weight:800; margin-top:0.25rem;">District 1 pickup zone</div>
    </div>
    <div style="font-size:0.86rem; opacity:0.9;">{len(results)} rescue options around ({st.session_state.user_lat:.4f}, {st.session_state.user_lng:.4f})</div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
        category_options = ["All"] + sorted({item["category"] for item in results})
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox("Category", category_options, key="result_category_filter")
        with col2:
            max_distance = st.slider("Distance", min_value=1, max_value=5, value=3, format="%d km")
        col3, col4 = st.columns(2)
        with col3:
            max_price = st.slider("Max price", min_value=10000, max_value=60000, value=50000, step=5000, format="%d VND")
        with col4:
            min_quantity = st.selectbox("Quantity", [1, 2, 3, 5], key="result_quantity_filter")
        col5, col6 = st.columns(2)
        with col5:
            pickup_filter = st.selectbox("Pickup time", ["Any", "20:00", "21:00", "22:00"], key="result_pickup_filter")
        with col6:
            best_before_filter = st.selectbox("Best-before", ["Any", "Tonight", "Tomorrow"], key="result_best_before_filter")
        st.caption("Filters are intentionally simple for the MVP demo.")
        st.markdown('</div>', unsafe_allow_html=True)

    filtered = [
        item
        for item in results
        if (category_filter == "All" or item["category"] == category_filter)
        and item["distance_km"] <= max_distance
        and item["price"] <= max_price
        and item["quantity"] >= min_quantity
        and (pickup_filter == "Any" or pickup_filter.lower() in item["pickup_window"].lower())
        and (best_before_filter == "Any" or best_before_filter.lower() in item["best_before"].lower())
    ]

    if not filtered:
        st.info("No rescue food matches those filters. Try expanding distance or price.")

    for index, item in enumerate(filtered):
        savings = max(0, int(item["original_price"] or 0) - int(item["price"] or 0))
        st.markdown(
            f"""
<div class="result-card">
    <div style="display:flex; gap:0.8rem; align-items:flex-start;">
        <div style="width:3.2rem; height:3.2rem; border-radius:12px; background:#E6F7EE; color:#007A2F; display:flex; align-items:center; justify-content:center; font-weight:800; flex:0 0 auto;">{category_icon(item['category'])}</div>
        <div style="flex:1; min-width:0;">
            <div class="result-title">{item['name']}</div>
            <div class="result-meta">{item['store_name']} - {item['distance_km']:.1f} km away</div>
            <div class="price-row">
                <span class="rescue-price">{vnd(item['price'])}</span>
                <span class="original-price">{vnd(item['original_price'])}</span>
            </div>
            <div class="result-meta">Save {vnd(savings)}</div>
        </div>
    </div>
    <div class="info-grid">
        <div class="info-pill">Pickup: {item['pickup_window']}</div>
        <div class="info-pill">{item['best_before']}</div>
        <div class="info-pill">Qty left: {item['quantity']}</div>
        <div class="info-pill">{item['category']}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("View rescue item", key=f"view_user_result_{item['id']}_{index}", use_container_width=True):
            choose_food(item)

    if st.button("Back to search", use_container_width=True):
        navigate("UserHome")


# ============================================================
# PAGE: FOOD DETAIL
# ============================================================
def page_food_detail():
    item = st.session_state.selected_food
    if not item:
        st.warning("Choose a rescue food item first.")
        if st.button("Back to results", use_container_width=True):
            navigate("UserResults")
        return

    stock = max(1, int(item.get("quantity") or 1))
    if st.session_state.selected_quantity > stock:
        st.session_state.selected_quantity = stock

    savings = max(0, int(item.get("original_price") or 0) - int(item.get("price") or 0))
    discount = int((savings / int(item.get("original_price") or 1)) * 100) if item.get("original_price") else 0

    st.markdown(
        f"""
<div class="user-hero">
    <div style="font-size:0.8rem; font-weight:700; opacity:0.9; text-transform:uppercase; letter-spacing:0.04em;">LoopBite</div>
    <h1>{item['name']}</h1>
    <p>{item['store_name']} - {item['distance_km']:.1f} km away</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="result-card">
    <div class="detail-photo">{category_icon(item['category'])}</div>
    <div class="result-title">{item['name']}</div>
    <div class="result-meta">{item['store_name']} - {item['store_address']}</div>
    <div class="price-row">
        <span class="rescue-price">{vnd(item['price'])}</span>
        <span class="original-price">{vnd(item['original_price'])}</span>
    </div>
    <div class="result-meta">Save {vnd(savings)}{f' ({discount}% off)' if discount else ''}</div>
    <div class="info-grid">
        <div class="info-pill">Category: {item['category']}</div>
        <div class="info-pill">Qty left: {stock}</div>
        <div class="info-pill">Pickup: {item['pickup_window']}</div>
        <div class="info-pill">{item['best_before']}</div>
    </div>
    <div class="note-box"><strong>Merchant quality note:</strong><br>{item['quality_note']}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.number_input(
        "Quantity to reserve",
        min_value=1,
        max_value=stock,
        step=1,
        key="selected_quantity",
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back to results", use_container_width=True):
            navigate("UserResults")
    with c2:
        if st.button("Reserve", type="primary", use_container_width=True):
            navigate("ReservationReview")


# ============================================================
# PAGE: RESERVATION REVIEW
# ============================================================
def page_reservation_review():
    item = st.session_state.selected_food
    if not item:
        st.warning("Choose a rescue food item first.")
        if st.button("Back to search", use_container_width=True):
            navigate("UserHome")
        return

    quantity = int(st.session_state.selected_quantity or 1)
    total = int(float(item.get("price") or 0) * quantity)

    st.markdown(
        """
<div class="user-hero">
    <div style="font-size:0.8rem; font-weight:700; opacity:0.9; text-transform:uppercase; letter-spacing:0.04em;">LoopBite</div>
    <h1>Review reservation</h1>
    <p>Confirm pickup and payment before holding this rescue item.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="result-card">
    <div class="result-title">{item['name']}</div>
    <div class="result-meta">{item['store_name']} - {item['store_address']}</div>
    <div class="review-row"><span class="review-label">Quantity</span><span class="review-value">{quantity}</span></div>
    <div class="review-row"><span class="review-label">Pickup window</span><span class="review-value">{item['pickup_window']}</span></div>
    <div class="review-row"><span class="review-label">Best-before</span><span class="review-value">{item['best_before']}</span></div>
    <div class="review-row"><span class="review-label">Unit price</span><span class="review-value">{vnd(item['price'])}</span></div>
    <div class="review-row"><span class="review-label">Total</span><span class="review-value">{vnd(total)}</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    pickup_options = ["Pick up at store", "Mock delivery (demo only)"]
    st.radio("Pickup method", pickup_options, key="pickup_method")
    if st.session_state.pickup_method.startswith("Mock delivery"):
        st.info("Delivery is shown for demo only. Store pickup is the MVP path.")

    payment_options = ["Pay at counter", "Mock online payment"]
    st.radio("Payment method", payment_options, key="payment_method")
    if st.session_state.payment_method == "Mock online payment":
        st.info("Online payment is mocked for the hackathon demo.")

    existing = st.session_state.active_reservation
    if existing and existing.get("item", {}).get("id") == item.get("id"):
        st.success(f"Reservation held. Pickup code: {existing['pickup_code']}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back to item", use_container_width=True):
            navigate("FoodDetail")
    with c2:
        if st.button("Confirm reservation", type="primary", use_container_width=True):
            st.session_state.active_reservation = {
                "pickup_code": make_pickup_code(),
                "status": "Reserved",
                "item": item,
                "quantity": quantity,
                "pickup_method": st.session_state.pickup_method,
                "payment_method": st.session_state.payment_method,
                "total": total,
                "customer": "Demo customer",
            }
            navigate("PickupConfirmation")


# ============================================================
# PAGE: CONFIRMATION / PICKUP CODE
# ============================================================
def page_pickup_confirmation():
    reservation = st.session_state.active_reservation
    if not reservation:
        st.warning("No active reservation yet.")
        if st.button("Back to search", use_container_width=True):
            navigate("UserHome")
        return

    item = reservation["item"]

    st.markdown(
        """
<div class="user-hero">
    <div style="font-size:0.8rem; font-weight:700; opacity:0.9; text-transform:uppercase; letter-spacing:0.04em;">LoopBite</div>
    <h1>Reservation confirmed</h1>
    <p>Show this pickup code at the counter during the pickup window.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="pickup-code">
    <div style="font-size:0.82rem; opacity:0.82; font-weight:700; text-transform:uppercase;">Pickup code</div>
    <div class="pickup-code-value">{reservation['pickup_code']}</div>
</div>
<div class="result-card">
    <div class="result-title">{item['name']}</div>
    <div class="result-meta">{item['store_name']} - {item['store_address']}</div>
    <div class="review-row"><span class="review-label">Pickup time</span><span class="review-value">{item['pickup_window']}</span></div>
    <div class="review-row"><span class="review-label">Quantity</span><span class="review-value">{reservation['quantity']}</span></div>
    <div class="review-row"><span class="review-label">Total price</span><span class="review-value">{vnd(reservation['total'])}</span></div>
    <div class="review-row"><span class="review-label">Payment</span><span class="review-value">{reservation['payment_method']}</span></div>
    <div class="review-row"><span class="review-label">Order status</span><span class="review-value">{reservation['status']}</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back to Search", use_container_width=True):
            navigate("UserHome")
    with c2:
        if st.button("Open Merchant Portal", type="primary", use_container_width=True):
            set_mode("Merchant Portal")
# ============================================================
# BOTTOM NAV
# ============================================================
def render_bottom_nav():
    pages = [
        ("Dashboard", "🏠"),
        ("Post", "➕"),
        ("Published", "📋"),
        ("Completed", "✅"),
        ("Profile", "👤"),
    ]
    cols = st.columns(len(pages))
    for col, (name, icon) in zip(cols, pages):
        with col:
            is_active = st.session_state.page == name
            label = f"**{icon}**" if is_active else icon
            if st.button(label, key=f"nav_{name}", use_container_width=True):
                navigate(name)


# ============================================================
# PAGE: DASHBOARD
# ============================================================
def page_dashboard():
    # Top bar with greeting
    merchant = api.get_merchant(DEMO_MERCHANT_ID) or {}
    merchant_name = merchant.get("name", "FamilyMart")
    merchant_addr = merchant.get("address", "")

    # API status banner
    if not API_OK:
        st.error("🔴 Backend offline. Không thể kết nối http://127.0.0.1:8000")

    # Load real data from API
    foods = _cached_food(DEMO_MERCHANT_ID)
    available_foods = [f for f in foods if (f.get("quantity") or 0) > 0]
    low_stock = sorted(
        [f for f in available_foods if (f.get("quantity") or 0) <= 3],
        key=lambda x: x.get("quantity") or 0,
    )
    total_items = sum((f.get("quantity") or 0) for f in available_foods)
    total_value = sum((f.get("price") or 0) * (f.get("quantity") or 0) for f in available_foods)

    st.markdown(
        f"""
<div class="top-bar">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:0.875rem; opacity:0.9;">Good Morning 👋</div>
            <div style="font-size:1.25rem; font-weight:700;">{merchant_name} - District 1</div>
        </div>
        <div style="font-size:1.75rem;">🔔</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Stats cards
    st.markdown("### 📊 Today Overview")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Available Items", str(total_items), f"{len(available_foods)} listings")
    with c2:
        st.metric("Listing Value", api.fmt_vnd_short(total_value), "")

    c3, c4 = st.columns(2)
    with c3:
        st.metric("Active Listings", str(len(available_foods)), "")
    with c4:
        st.metric("Low Stock", str(len(low_stock)), "")

    st.divider()

    # New reservation queue from the user demo flow
    st.markdown("### New Reservation")
    reservation = st.session_state.active_reservation
    if reservation:
        order_item = apply_quantity_override(reservation["item"])
        status_class = "badge-gray" if reservation["status"] == "Picked Up" else "badge-active"
        stock_label = "Sold Out" if int(order_item.get("quantity") or 0) == 0 else f"{order_item.get('quantity', 0)} left"
        st.markdown(
            f"""
<div class="reservation-card">
    <div style="display:flex; justify-content:space-between; gap:0.75rem; align-items:flex-start;">
        <div style="flex:1; min-width:0;">
            <div style="font-size:0.78rem; color:#007A2F; font-weight:800; text-transform:uppercase;">Pickup code {reservation['pickup_code']}</div>
            <div class="result-title" style="margin-top:0.25rem;">{order_item['name']}</div>
            <div class="result-meta">{reservation['customer']} - Qty {reservation['quantity']}</div>
        </div>
        <span class="badge {status_class}">{reservation['status']}</span>
    </div>
    <div class="info-grid">
        <div class="info-pill">Pickup: {order_item['pickup_window']}</div>
        <div class="info-pill">Total: {vnd(reservation['total'])}</div>
        <div class="info-pill">Payment: {reservation['payment_method']}</div>
        <div class="info-pill">Stock after pickup: {stock_label}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        if reservation["status"] == "Picked Up":
            st.success("Pickup confirmed. Order status is Picked Up.")
        elif st.button("Confirm Pickup", type="primary", use_container_width=True):
            confirm_pickup()
            st.rerun()
    else:
        st.markdown(
            """
<div class="empty-state">
    No new reservations yet. Create a reservation from the User App to show the merchant handoff in the demo.
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    # Active listings preview (real data)
    st.markdown("### 📦 Active Listings")

    if not available_foods:
        st.info("Chưa có món nào. Tap ➕ để đăng món mới!")
    else:
        for food in available_foods[:5]:
            emoji = api.category_emoji(food.get("category", ""))
            remaining = api.time_until(food.get("expiry_time"))
            st.markdown(
                f"""
<div class="food-card">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="font-size:2.5rem;">{emoji}</div>
        <div style="flex:1;">
            <div style="font-weight:600;">{food.get('name', '—')}</div>
            <div style="font-size:0.8rem; color:#6B7280;">
                Qty: {food.get('quantity', 0)} · ⏰ {remaining}
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{api.fmt_vnd_short(food.get('price', 0))}</div>
            <span class="badge badge-active" style="margin-top:0.25rem;">Active</span>
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.divider()

    # Low stock alerts (real data)
    st.markdown("### ⚠️ Low Stock Alert")
    if not low_stock:
        st.success("✅ All listings have healthy stock")
    else:
        for food in low_stock[:3]:
            emoji = api.category_emoji(food.get("category", ""))
            remaining = api.time_until(food.get("expiry_time"))
            st.markdown(
                f"""
<div class="food-card" style="border-left: 4px solid #F4A261;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="font-size:2rem;">{emoji}</div>
            <div>
                <div style="font-weight:600;">{food.get('name', '—')}</div>
                <div style="font-size:0.875rem; color:#6B7280;">⏰ {remaining}</div>
            </div>
        </div>
        <span class="badge badge-danger">{food.get('quantity', 0)} left</span>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    render_bottom_nav()


# ============================================================
# PAGE: POST RESCUE ITEM
# ============================================================
def page_post():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">Post Rescue Item</h2>
    <p style="margin:0.25rem 0 0 0; font-size:0.875rem; opacity:0.9;">
        Publish surplus food in under 60 seconds.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### Item basics")
    food_name = st.text_input("Food name *", placeholder="e.g., Butter Croissant Rescue Box")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Category *",
            ["Pastry", "Bread", "Noodles", "Snacks", "Packaged meal", "Drink", "Other"],
        )
    with col2:
        quantity = st.number_input("Quantity *", min_value=1, max_value=100, value=3)

    st.markdown("### Pricing")
    col3, col4 = st.columns(2)
    with col3:
        original_price = st.number_input("Original price (VND) *", min_value=0, value=42000, step=1000)
    with col4:
        rescue_price = st.number_input("Rescue price (VND) *", min_value=0, value=18000, step=1000)

    discount = int((1 - rescue_price / original_price) * 100) if original_price > 0 else 0
    if discount > 0:
        st.success(f"Discount: {discount}% off")

    st.markdown("### Pickup and best-before")
    exp_date = st.date_input("Best-before date *", datetime.now() + timedelta(hours=4))
    t1, t2 = st.columns(2)
    with t1:
        pickup_start = st.time_input("Pickup start *", datetime.now() + timedelta(hours=2))
    with t2:
        pickup_end = st.time_input("Pickup end *", datetime.now() + timedelta(hours=4))
    best_before_time = st.time_input("Best-before time *", datetime.now() + timedelta(hours=5))

    st.markdown("### Notes")
    uploaded = st.file_uploader("Food photo", type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, caption="Preview", use_container_width=True)

    quality_note = st.text_area(
        "Quality note *",
        placeholder="e.g., Baked this morning, packed after display period.",
        height=80,
    )
    buyer_note = st.text_area(
        "Note for buyers",
        placeholder="e.g., Please pick up at the counter and show the pickup code.",
        height=70,
    )

    st.divider()

    cb, cc = st.columns([1, 1])
    with cb:
        if st.button("Cancel", use_container_width=True):
            navigate("Dashboard")
    with cc:
        if st.button("Publish Listing", type="primary", use_container_width=True):
            errors = []
            if not food_name.strip():
                errors.append("Food name is required.")
            if original_price <= 0:
                errors.append("Original price must be greater than 0.")
            if rescue_price <= 0:
                errors.append("Rescue price must be greater than 0.")
            if rescue_price >= original_price:
                errors.append("Rescue price must be lower than original price.")
            if pickup_end <= pickup_start:
                errors.append("Pickup end must be after pickup start.")
            if not quality_note.strip():
                errors.append("Quality note is required.")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                exp_dt = datetime.combine(exp_date, best_before_time)
                pickup_window = f"Today {pickup_start.strftime('%H:%M')}-{pickup_end.strftime('%H:%M')}"
                payload = {
                    "merchant_id": DEMO_MERCHANT_ID,
                    "name": food_name.strip(),
                    "category": category,
                    "price": float(rescue_price),
                    "quantity": int(quantity),
                    "status": "available",
                    "expiry_time": exp_dt.isoformat(),
                }

                result = api.create_food(payload) if API_OK else None
                if result:
                    _cached_food.clear()
                    result["original_price"] = int(original_price)
                    result["pickup_window"] = pickup_window
                    result["quality_note"] = quality_note.strip()
                    st.success(f"Published via API: {result.get('name')}")
                else:
                    result = add_mock_listing(
                        payload,
                        original_price=int(original_price),
                        pickup_window=pickup_window,
                        quality_note=quality_note.strip(),
                    )
                    st.success(f"Published in demo mode: {result.get('name')}")

                if buyer_note.strip():
                    st.caption(f"Buyer note: {buyer_note.strip()}")
                st.balloons()
                import time as _t
                _t.sleep(1)
                navigate("Published")

    render_bottom_nav()

# ============================================================
# PAGE: PUBLISHED (ACTIVE LISTINGS)
# ============================================================
def page_published():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">📋 Active Listings</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    if not API_OK:
        st.error("🔴 Backend offline. Không thể tải listings.")

    # Load from API
    foods = _cached_food(DEMO_MERCHANT_ID)
    available = [f for f in foods if (f.get("quantity") or 0) > 0]

    # Normalize to UI shape
    listings = [
        {
            "id": f.get("id"),
            "name": f.get("name", "—"),
            "qty": f.get("quantity", 0),
            "price": api.fmt_vnd_short(f.get("price", 0)),
            "exp": api.time_until(f.get("expiry_time")),
            "status": "Active",
            "emoji": api.category_emoji(f.get("category", "")),
        }
        for f in available
    ]

    tabs = st.tabs([f"🔵 All ({len(listings)})", f"🟢 Active ({len(listings)})"])

    with tabs[0]:
        render_listings(listings, prefix="all")
    with tabs[1]:
        render_listings(listings, prefix="active")

    render_bottom_nav()


def render_listings(listings, prefix=""):
    if not listings:
        st.info("No listings yet. Tap ➕ to create one!")
        return

    for item in listings:
        status_class = "badge-active" if item["status"] == "Confirmed" else "badge-warn"

        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="font-size:2.5rem;">{item['emoji']}</div>
        <div style="flex:1;">
            <div style="font-weight:600;">{item['name']}</div>
            <div style="font-size:0.8rem; color:#6B7280;">
                Qty: {item['qty']} · ⏰ {item['exp']} left
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{item['price']}</div>
            <span class="badge {status_class}" style="margin-top:0.25rem;">
                {item['status']}
            </span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button("View Details", key=f"view_{prefix}_{item['id']}"):
            pass


# ============================================================
# PAGE: COMPLETED
# ============================================================
def page_completed():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">✅ Completed Orders</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    if not API_OK:
        st.error("🔴 Backend offline.")

    # Load foods and treat expired ones as "completed" sales (heuristic)
    foods = _cached_food(DEMO_MERCHANT_ID)
    sold = [f for f in foods if (f.get("quantity") or 0) == 0]
    total_revenue = sum((f.get("price") or 0) * 5 for f in sold)  # demo multiplier
    total_items_sold = len(sold) * 5

    # Summary
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Listings Closed", str(len(sold)))
    with c2:
        st.metric("Items Sold", str(total_items_sold))
    with c3:
        st.metric("Revenue", api.fmt_vnd_short(total_revenue))

    st.divider()

    if not sold:
        st.info("Chưa có đơn hoàn thành.")
    else:
        for order in sold[:20]:
            st.markdown(
                f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between; align-items:start;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="font-size:2rem;">{api.category_emoji(order.get('category', ''))}</div>
            <div>
                <div style="font-weight:600;">{order.get('name', '—')}</div>
                <div style="font-size:0.875rem; color:#6B7280;">📦 FamilyMart - District 1</div>
                <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">{api.time_until(order.get('expiry_time'))}</div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{api.fmt_vnd_short(order.get('price', 0))}</div>
            <span class="badge badge-gray" style="margin-top:0.25rem;">✓ Sold</span>
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    render_bottom_nav()


# ============================================================
# PAGE: PROFILE
# ============================================================
def page_profile():
    merchant = api.get_merchant(DEMO_MERCHANT_ID) or {}
    merchant_name = merchant.get("name", "FamilyMart")
    merchant_addr = merchant.get("address", "")

    st.markdown(
        f"""
<div class="top-bar">
    <h2 style="margin:0; color:white;">👤 Profile</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    # Store info
    st.markdown(
        f"""
<div class="food-card" style="text-align:center; padding:1.5rem;">
    <div style="font-size:4rem;">🏪</div>
    <div style="font-weight:700; font-size:1.25rem; margin-top:0.5rem;">
        {merchant_name} - District 1
    </div>
    <div style="font-size:0.875rem; color:#6B7280;">Merchant ID: FM-{DEMO_MERCHANT_ID:03d}</div>
    <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">📍 {merchant_addr or "—"}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Live stats from API
    foods = _cached_food(DEMO_MERCHANT_ID)
    total_listings = len(foods)
    total_qty = sum((f.get("quantity") or 0) for f in foods)

    st.markdown("### 📊 This Month")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Listings", str(total_listings))
        st.metric("Total Items", str(total_qty))
    with c2:
        st.metric("API Status", "🟢 Online" if API_OK else "🔴 Offline")
        st.metric("Backend", "127.0.0.1:8000")

    st.divider()

    # Menu items
    menu = [
        ("🏪", "Store Information"),
        ("📍", "Locations (3)"),
        ("💰", "Payout Settings"),
        ("🔔", "Notifications"),
        ("❓", "Help & Support"),
        ("⚙️", "Settings"),
        ("🚪", "Logout"),
    ]

    for icon, label in menu:
        st.markdown(
            f"""
<div class="food-card" style="padding:0.75rem 1rem;">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="font-size:1.5rem;">{icon}</div>
        <div style="flex:1; font-weight:500;">{label}</div>
        <div style="color:#9CA3AF;">›</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    render_bottom_nav()


# ============================================================
# ROUTER
# ============================================================
USER_ROUTES = {"UserHome", "UserResults", "FoodDetail", "ReservationReview", "PickupConfirmation"}
MERCHANT_ROUTES = {"Dashboard", "Post", "Published", "Completed", "Profile"}

ROUTES = {
    "UserHome": page_user_home,
    "UserResults": page_user_results,
    "FoodDetail": page_food_detail,
    "ReservationReview": page_reservation_review,
    "PickupConfirmation": page_pickup_confirmation,
    "Dashboard": page_dashboard,
    "Post": page_post,
    "Published": page_published,
    "Completed": page_completed,
    "Profile": page_profile,
}

# Render selected page
if st.session_state.mode == "User App" and st.session_state.page not in USER_ROUTES:
    st.session_state.page = "UserHome"
elif st.session_state.mode == "Merchant Portal" and st.session_state.page not in MERCHANT_ROUTES:
    st.session_state.page = "Dashboard"

render_mode_switch()
page_fn = ROUTES.get(st.session_state.page, page_user_home)
page_fn()

