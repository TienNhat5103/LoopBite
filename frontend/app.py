"""
FamilyMart Rescue - Merchant Dashboard
Mobile-first Streamlit UI for merchants to manage rescue food listings.
"""
import streamlit as st
from datetime import datetime, timedelta
import random

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
if "reservations" not in st.session_state:
    st.session_state.reservations = []


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
    st.markdown(
        """
<div class="top-bar">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:0.875rem; opacity:0.9;">Good Morning 👋</div>
            <div style="font-size:1.25rem; font-weight:700;">FamilyMart - District 1</div>
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
        st.metric("Rescued Items", "12", "+3")
    with c2:
        st.metric("Revenue Saved", "450K", "+120K")

    c3, c4 = st.columns(2)
    with c3:
        st.metric("Active Listings", "5", "")
    with c4:
        st.metric("Pending Pickup", "2", "")

    st.divider()

    # New reservations
    st.markdown("### 🔔 New Reservation Requests")

    new_reqs = [
        {
            "id": 1,
            "customer": "Nguyễn Văn A",
            "items": "3 Onigiri, 2 Sandwich",
            "time": "10 mins ago",
            "total": "85,000đ",
        },
        {
            "id": 2,
            "customer": "Trần Thị B",
            "items": "1 Bento Set",
            "time": "25 mins ago",
            "total": "45,000đ",
        },
    ]

    for req in new_reqs:
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between; align-items:start;">
        <div style="flex:1;">
            <div style="font-weight:600;">{req['customer']}</div>
            <div style="font-size:0.875rem; color:#6B7280; margin-top:0.25rem;">
                {req['items']}
            </div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">
                {req['time']}
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{req['total']}</div>
            <span class="badge badge-warn" style="margin-top:0.25rem;">Pending</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        ca, cb = st.columns(2)
        with ca:
            if st.button("✓ Accept", key=f"acc_{req['id']}", type="primary"):
                st.success(f"Accepted {req['customer']}'s reservation")
        with cb:
            if st.button("✗ Decline", key=f"dec_{req['id']}"):
                st.warning(f"Declined {req['customer']}'s reservation")

    st.divider()

    # Low stock alerts
    st.markdown("### ⚠️ Low Stock Alert")
    st.markdown(
        """
<div class="food-card" style="border-left: 4px solid #F4A261;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-weight:600;">Onigiri - Salmon</div>
            <div style="font-size:0.875rem; color:#6B7280;">Expires in 2 hours</div>
        </div>
        <span class="badge badge-danger">2 left</span>
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
            if food_name:
                st.success("✅ Listing published!")
                st.balloons()
                navigate("Dashboard")
            else:
                st.error("Please enter food name")

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

    tabs = st.tabs(["🔵 All", "🟡 Pending", "🟢 Confirmed"])

    listings = [
        {"id": 1, "name": "Onigiri Salmon", "qty": 2, "price": "15K", "exp": "2h", "status": "Confirmed", "emoji": "🍙"},
        {"id": 2, "name": "Sandwich Egg Mayo", "qty": 4, "price": "12K", "exp": "5h", "status": "Pending", "emoji": "🥪"},
        {"id": 3, "name": "Bento Set A", "qty": 1, "price": "45K", "exp": "3h", "status": "Confirmed", "emoji": "🍱"},
        {"id": 4, "name": "Caesar Salad", "qty": 3, "price": "25K", "exp": "6h", "status": "Pending", "emoji": "🥗"},
        {"id": 5, "name": "Melon Bread", "qty": 5, "price": "10K", "exp": "8h", "status": "Confirmed", "emoji": "🍞"},
    ]

    with tabs[0]:
        render_listings(listings, prefix="all")
    with tabs[1]:
        render_listings([l for l in listings if l["status"] == "Pending"], prefix="pend")
    with tabs[2]:
        render_listings([l for l in listings if l["status"] == "Confirmed"], prefix="conf")

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
            navigate("Reservation")


# ============================================================
# PAGE: RESERVATION DETAILS
# ============================================================
def page_reservation():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">📄 Reservation Details</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("← Back"):
        navigate("Published")

    # Reservation header
    st.markdown(
        """
<div class="food-card" style="border-left: 4px solid #00A040;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:0.75rem; color:#6B7280;">Order #FM-2024-001</div>
            <div style="font-weight:700; font-size:1.1rem; margin-top:0.25rem;">
                Nguyễn Văn A
            </div>
        </div>
        <span class="badge badge-active">Confirmed</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Customer info
    st.markdown("### 👤 Customer Info")
    st.markdown(
        """
<div class="food-card">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="font-size:2.5rem;">👤</div>
        <div>
            <div style="font-weight:600;">Nguyễn Văn A</div>
            <div style="font-size:0.8rem; color:#6B7280;">📞 0901-234-567</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Order items
    st.markdown("### 🛒 Order Items")
    items = [
        {"name": "Onigiri Salmon", "qty": 3, "price": "15,000đ"},
        {"name": "Sandwich Egg Mayo", "qty": 2, "price": "12,000đ"},
    ]

    for item in items:
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between;">
        <div>
            <div style="font-weight:600;">{item['name']}</div>
            <div style="font-size:0.8rem; color:#6B7280;">Qty: {item['qty']}</div>
        </div>
        <div style="font-weight:600;">{item['price']}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # Total
    st.markdown(
        """
<div class="food-card" style="background:#E6F7EE;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="font-weight:700;">Total</div>
        <div style="font-weight:700; font-size:1.25rem; color:#00A040;">69,000đ</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Pickup info
    st.markdown("### ⏰ Pickup Time")
    st.info("Today, 14:30 - 15:00")

    st.markdown("### 📍 Pickup Location")
    st.markdown(
        """
<div class="food-card">
    <div style="font-size:0.875rem;">
        🏪 FamilyMart - District 1<br>
        📍 20 Lê Thánh Tôn, P. Sài Gòn, Tp. HCM
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    # Action buttons
    ca, cb = st.columns(2)
    with ca:
        if st.button("📞 Call", use_container_width=True):
            st.info("Calling 0901-234-567...")
    with cb:
        if st.button("✓ Mark Completed", type="primary", use_container_width=True):
            st.success("Order completed!")
            navigate("Completed")

    render_bottom_nav()


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

    completed = [
        {"id": 1, "name": "Bento Set A", "customer": "Lê Văn C", "time": "2 hours ago", "amount": "45,000đ"},
        {"id": 2, "name": "Onigiri x5", "customer": "Phạm Thị D", "time": "Yesterday", "amount": "75,000đ"},
        {"id": 3, "name": "Sandwich x3", "customer": "Hoàng Văn E", "time": "Yesterday", "amount": "36,000đ"},
        {"id": 4, "name": "Salad Mix", "customer": "Vũ Thị F", "time": "2 days ago", "amount": "50,000đ"},
    ]

    # Summary
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Orders", "12")
    with c2:
        st.metric("Items", "47")
    with c3:
        st.metric("Revenue", "1.2M")

    st.divider()

    for order in completed:
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between; align-items:start;">
        <div>
            <div style="font-weight:600;">{order['name']}</div>
            <div style="font-size:0.875rem; color:#6B7280;">👤 {order['customer']}</div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">{order['time']}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{order['amount']}</div>
            <span class="badge badge-gray" style="margin-top:0.25rem;">✓ Done</span>
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
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">👤 Profile</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    # Store info
    st.markdown(
        """
<div class="food-card" style="text-align:center; padding:1.5rem;">
    <div style="font-size:4rem;">🏪</div>
    <div style="font-weight:700; font-size:1.25rem; margin-top:0.5rem;">
        FamilyMart - District 1
    </div>
    <div style="font-size:0.875rem; color:#6B7280;">Merchant ID: FM-D1-001</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 This Month")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Sales", "3.2M")
        st.metric("Items Sold", "127")
    with c2:
        st.metric("CO₂ Saved", "85kg")
        st.metric("Customers", "63")

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
    "Reservation": page_reservation,
    "Completed": page_completed,
    "Profile": page_profile,
}

# Render selected page
page_fn = ROUTES.get(st.session_state.page, page_dashboard)
page_fn()