"""
FamilyMart Rescue - Merchant Dashboard
Mobile-first Streamlit UI for merchants to manage rescue food listings.
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
    page_title="FamilyMart Rescue",
    page_icon="🟢",
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
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def navigate(page_name: str):
    """Change current page."""
    st.session_state.page = page_name
    st.rerun()


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
    <h2 style="margin:0; color:white;">➕ Post Rescue Item</h2>
    <p style="margin:0.25rem 0 0 0; font-size:0.875rem; opacity:0.9;">
        Save food, save the planet 🌍
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### Food Details")

    food_name = st.text_input("Food Name *", placeholder="e.g., Onigiri Salmon")
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Category *",
            ["🍙 Onigiri", "🥪 Sandwich", "🍱 Bento", "🥗 Salad", "🍞 Bread", "🥤 Drink", "Other"],
        )
    with col2:
        quantity = st.number_input("Quantity *", min_value=1, max_value=100, value=3)

    col3, col4 = st.columns(2)
    with col3:
        original_price = st.number_input("Original Price (đ) *", min_value=0, value=35000, step=1000)
    with col4:
        rescue_price = st.number_input("Rescue Price (đ) *", min_value=0, value=15000, step=1000)

    discount = int((1 - rescue_price / original_price) * 100) if original_price > 0 else 0
    if discount > 0:
        st.success(f"💰 Discount: {discount}% off")

    st.markdown("### ⏰ Expiration")
    exp_date = st.date_input("Best before date", datetime.now() + timedelta(hours=4))
    exp_time = st.time_input("Best before time", datetime.now() + timedelta(hours=4))

    st.markdown("### 📸 Photo")
    uploaded = st.file_uploader("Upload food photo", type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, caption="Preview", use_container_width=True)

    st.markdown("### 📝 Description")
    description = st.text_area(
        "Additional notes",
        placeholder="e.g., Packed this morning, still fresh...",
        height=80,
    )

    st.divider()

    cb, cc = st.columns([1, 1])
    with cb:
        if st.button("Cancel", use_container_width=True):
            navigate("Dashboard")
    with cc:
        if st.button("✓ Publish Listing", type="primary", use_container_width=True):
            if not food_name.strip():
                st.error("Please enter food name")
            elif not API_OK:
                st.error("🔴 Backend offline. Cannot publish.")
            else:
                # Map category emoji to plain text label
                cat_label = category.split(" ", 1)[-1] if " " in category else category
                exp_dt = datetime.combine(exp_date, exp_time)
                payload = {
                    "merchant_id": DEMO_MERCHANT_ID,
                    "name": food_name.strip(),
                    "category": cat_label,
                    "price": float(rescue_price),
                    "quantity": int(quantity),
                    "status": "available",
                    "expiry_time": exp_dt.isoformat(),
                }
                result = api.create_food(payload)
                if result:
                    _cached_food.clear()
                    st.success(f"✅ Published: {result.get('name')} (id={result.get('id')})")
                    st.balloons()
                    import time as _t
                    _t.sleep(1)
                    navigate("Published")
                else:
                    st.error("Failed to publish. Check backend logs.")

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
ROUTES = {
    "Dashboard": page_dashboard,
    "Post": page_post,
    "Published": page_published,
    "Completed": page_completed,
    "Profile": page_profile,
}

# Render selected page
page_fn = ROUTES.get(st.session_state.page, page_dashboard)
page_fn()