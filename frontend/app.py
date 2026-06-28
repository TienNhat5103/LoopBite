"""
LoopBite MVP - Streamlit demo for users and merchants.
"""
import streamlit as st
from datetime import datetime, timedelta
import random

try:
    import pydeck as pdk
except ImportError:
    pdk = None

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
.map-legend {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
    margin: -0.25rem 0 0.9rem 0;
    display: flex;
    gap: 0.85rem;
    align-items: center;
    flex-wrap: wrap;
    color: var(--text-gray);
    font-size: 0.78rem;
}
.legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 650;
}
.legend-dot {
    width: 0.7rem;
    height: 0.7rem;
    border-radius: 999px;
    display: inline-block;
}
.legend-user { background: #F6C85F; }
.legend-store { background: #1FBF75; }
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
.dish-image-wrap {
    width: 4.2rem;
    height: 4.2rem;
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    flex: 0 0 auto;
    background: #F3F7F4;
    border: 1px solid #E8F0EA;
}
.dish-thumb {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
.dish-index {
    position: absolute;
    top: 0.35rem;
    left: 0.35rem;
    width: 1.25rem;
    height: 1.25rem;
    border-radius: 999px;
    background: #102A1E;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 800;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
.quick-search-card {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    background: #FFFFFF;
    margin-bottom: 0.45rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.quick-search-image {
    width: 100%;
    height: 4.2rem;
    object-fit: cover;
    display: block;
}
.quick-search-title {
    padding: 0.45rem 0.55rem 0.55rem 0.55rem;
    font-size: 0.82rem;
    font-weight: 750;
    color: var(--text-dark);
    text-align: center;
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
    height: 12rem;
    border-radius: 12px;
    overflow: hidden;
    background: #F3F7F4;
    margin-bottom: 0.85rem;
    border: 1px solid #E8F0EA;
}
.detail-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
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
.delivery-panel {
    background: #F3FAF6;
    border: 1px solid #BFEBD1;
    border-radius: 12px;
    padding: 0.9rem;
    margin: 0.55rem 0 1rem 0;
}
.delivery-provider-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
    margin-top: 0.65rem;
}
.delivery-provider-card {
    background: #FFFFFF;
    border: 1px solid #DDEBE3;
    border-radius: 10px;
    padding: 0.65rem 0.5rem;
    text-align: center;
}
.delivery-provider-logo {
    width: 2.15rem;
    height: 2.15rem;
    border-radius: 999px;
    background: #102A1E;
    color: #FFFFFF;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 850;
    margin-bottom: 0.35rem;
}
.delivery-provider-name {
    font-size: 0.78rem;
    font-weight: 800;
    color: var(--text-dark);
}
.delivery-status {
    display: flex;
    gap: 0.7rem;
    align-items: center;
    margin-top: 0.75rem;
    background: #FFFFFF;
    border-radius: 10px;
    padding: 0.7rem;
}
.delivery-pulse {
    width: 0.85rem;
    height: 0.85rem;
    border-radius: 999px;
    background: #1FBF75;
    box-shadow: 0 0 0 6px rgba(31, 191, 117, 0.14);
    flex: 0 0 auto;
}
.delivery-status-title {
    font-size: 0.88rem;
    font-weight: 800;
    color: #075C2D;
}
.delivery-status-copy {
    font-size: 0.78rem;
    color: var(--text-gray);
    margin-top: 0.12rem;
}
.driver-hero-card {
    background: linear-gradient(135deg, #102A1E 0%, #0F8A4B 58%, #F6C85F 100%);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 1.15rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 10px 26px rgba(16, 42, 30, 0.18);
}
.driver-hero-card h2 {
    margin: 0.35rem 0 0 0;
    font-size: 1.55rem;
    line-height: 1.08;
    letter-spacing: 0;
}
.driver-route-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.driver-step-row {
    display: flex;
    gap: 0.75rem;
    padding: 0.5rem 0;
    align-items: flex-start;
}
.driver-step-dot {
    width: 1.35rem;
    height: 1.35rem;
    border-radius: 999px;
    background: #E6F7EE;
    color: #007A2F;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 900;
    flex: 0 0 auto;
}
.driver-step-title {
    font-size: 0.9rem;
    font-weight: 800;
    color: var(--text-dark);
}
.driver-step-copy {
    font-size: 0.8rem;
    color: var(--text-gray);
    margin-top: 0.1rem;
}
.driver-waiting-panel {
    background: #F3FAF6;
    border: 1px solid #BFEBD1;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.9rem;
}
.app-switch {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.55rem;
    margin: 0 0 0.9rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.app-switch-label {
    color: var(--text-gray);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.35rem;
}
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.7rem;
    margin: 0.75rem 0 1.1rem 0;
}
.dashboard-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.dashboard-card.primary {
    background: #F3FAF6;
    border-color: #BFEBD1;
}
.dashboard-label {
    color: var(--text-gray);
    font-size: 0.74rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.035em;
}
.dashboard-value {
    color: var(--text-dark);
    font-size: 1.55rem;
    font-weight: 900;
    line-height: 1.05;
    margin-top: 0.35rem;
}
.dashboard-hint {
    color: #007A2F;
    font-size: 0.78rem;
    font-weight: 750;
    margin-top: 0.35rem;
}
.dashboard-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-top: 1.1rem;
}
.dashboard-section-title h3 {
    margin: 0;
    font-size: 1.3rem;
    letter-spacing: 0;
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
if "delivery_provider" not in st.session_state:
    st.session_state.delivery_provider = "Grab"


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

def short_vnd(amount):
    try:
        value = int(float(amount))
    except (TypeError, ValueError):
        return "0 VND"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M VND"
    if value >= 1_000:
        return f"{value // 1_000}K VND"
    return f"{value} VND"
def render_app_switch():
    st.markdown(
        """
<div class="app-switch">
    <div class="app-switch-label">Choose app</div>
</div>
""",
        unsafe_allow_html=True,
    )
    user_col, merchant_col = st.columns(2)
    with user_col:
        label = "User App active" if st.session_state.mode == "User App" else "User App"
        if st.button(label, key="switch_user_app", use_container_width=True):
            if st.session_state.mode != "User App":
                set_mode("User App")
    with merchant_col:
        label = "Merchant active" if st.session_state.mode == "Merchant Portal" else "Merchant Portal"
        if st.button(label, key="switch_merchant_app", use_container_width=True):
            if st.session_state.mode != "Merchant Portal":
                set_mode("Merchant Portal")

def category_icon(category):
    cat = (category or "").lower()
    if any(word in cat for word in ["pastry", "bread", "bakery", "croissant"]):
        return "BA"
    if any(word in cat for word in ["noodle", "meal", "bento", "rice"]):
        return "ME"
    if any(word in cat for word in ["snack", "sweet"]):
        return "SN"
    return "FD"

FOOD_ART = {
    "pastry": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fff4cf"/><stop offset="1" stop-color="#dff7ea"/></linearGradient><linearGradient id="cr" x1="0" x2="1"><stop stop-color="#f7c45f"/><stop offset="1" stop-color="#b96a2f"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><circle cx="124" cy="23" r="28" fill="#1fbf75" opacity=".16"/><path d="M30 70c12-33 55-45 91-19-11 30-56 43-91 19z" fill="url(#cr)"/><path d="M43 66c13-11 29-14 49-9M61 79c18-5 32-13 45-28" stroke="#fff0c0" stroke-width="6" stroke-linecap="round" opacity=".7"/><ellipse cx="73" cy="91" rx="45" ry="8" fill="#102a1e" opacity=".12"/></svg>
""",
    "bread": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fff8dd"/><stop offset="1" stop-color="#e6f7ee"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><rect x="34" y="42" width="92" height="44" rx="20" fill="#c47a35"/><path d="M43 49c9-23 31-25 38 0 8-24 34-22 39 2" fill="#e7a85e"/><path d="M54 61h53M52 73h55" stroke="#fff1c9" stroke-width="6" stroke-linecap="round" opacity=".65"/><ellipse cx="80" cy="93" rx="48" ry="7" fill="#102a1e" opacity=".12"/></svg>
""",
    "noodles": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#e9fff3"/><stop offset="1" stop-color="#fff0c6"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><path d="M37 64h86l-10 31H47z" fill="#1fbf75"/><path d="M43 64c5 17 69 17 76 0" fill="#f6c85f"/><path d="M50 55c18-13 39 11 58-2M48 45c20 12 42-11 62 1M60 35c11 8 26-6 38 2" fill="none" stroke="#d98b3a" stroke-width="5" stroke-linecap="round"/><circle cx="108" cy="57" r="8" fill="#ef4444" opacity=".82"/></svg>
""",
    "snacks": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#f0fff6"/><stop offset="1" stop-color="#fff7d8"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><rect x="45" y="28" width="70" height="68" rx="12" fill="#f6c85f"/><path d="M45 43h70v18H45z" fill="#1fbf75"/><circle cx="66" cy="74" r="9" fill="#ffffff" opacity=".75"/><circle cx="91" cy="74" r="9" fill="#ffffff" opacity=".75"/><path d="M57 28l-10-13M103 28l10-13" stroke="#102a1e" stroke-width="5" stroke-linecap="round" opacity=".18"/></svg>
""",
    "late_night": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#eaf2ff"/><stop offset="1" stop-color="#fff2bf"/></linearGradient><linearGradient id="bag" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#243b7a"/><stop offset="1" stop-color="#1fbf75"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><circle cx="118" cy="28" r="15" fill="#f6c85f"/><circle cx="124" cy="23" r="15" fill="#eaf2ff"/><path d="M49 46h62l-6 48H55z" fill="url(#bag)"/><path d="M62 47c0-15 36-15 36 0" fill="none" stroke="#102a1e" stroke-width="7" stroke-linecap="round" opacity=".2"/><rect x="56" y="58" width="48" height="11" rx="5" fill="#f6c85f"/><circle cx="70" cy="81" r="7" fill="#fff6d6"/><circle cx="91" cy="81" r="7" fill="#fff6d6"/><path d="M31 33l5 7 8-3-5 7 5 7-8-3-5 7 1-8-7-4 8-1z" fill="#ffffff" opacity=".85"/></svg>
""",
    "meal": """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fff6d6"/><stop offset="1" stop-color="#e5f7ee"/></linearGradient></defs>
<rect width="160" height="120" rx="18" fill="url(#bg)"/><rect x="34" y="33" width="92" height="58" rx="14" fill="#102a1e" opacity=".9"/><rect x="43" y="42" width="37" height="40" rx="10" fill="#ffffff"/><rect x="86" y="42" width="31" height="18" rx="8" fill="#1fbf75"/><rect x="86" y="64" width="31" height="18" rx="8" fill="#f6c85f"/><circle cx="62" cy="62" r="12" fill="#f4a261"/></svg>
""",
}


def food_art_key(value):
    text = value.get("category", "") if isinstance(value, dict) else str(value or "")
    text = text.lower()
    if any(word in text for word in ["pastry", "croissant", "bakery"]):
        return "pastry"
    if "bread" in text:
        return "bread"
    if any(word in text for word in ["noodle", "rice", "meal", "bento"]):
        return "noodles" if "noodle" in text else "meal"
    if "late-night" in text or "late night" in text:
        return "late_night"
    if any(word in text for word in ["snack", "sweet"]):
        return "snacks"
    return "meal"


def svg_data_uri(svg):
    encoded = svg.strip().replace("#", "%23").replace("\n", "").replace('"', "'").replace(" ", "%20")
    return f"data:image/svg+xml;utf8,{encoded}"


def dish_image_src(value):
    return svg_data_uri(FOOD_ART[food_art_key(value)])


def render_quick_search_card(term):
    st.markdown(
        f"""
<div class="quick-search-card">
    <img class="quick-search-image" src="{dish_image_src(term)}" alt="{term.title()}" />
    <div class="quick-search-title">{term.title()}</div>
</div>
""",
        unsafe_allow_html=True,
    )

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
            "lat": 10.7793,
            "lng": 106.7018,
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
            "lat": 10.7758,
            "lng": 106.7044,
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
            "lat": 10.7732,
            "lng": 106.6984,
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
                    "lat": float(merchant.get("latitude") or merchant.get("lat") or st.session_state.user_lat + (0.003 * (len(rows) + 1))),
                    "lng": float(merchant.get("longitude") or merchant.get("lng") or st.session_state.user_lng + (0.003 * (len(rows) + 1))),
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


def map_marker_rows(results):
    sorted_results = sorted(results, key=lambda item: item.get("distance_km", 999))
    markers = [
        {
            "lat": st.session_state.user_lat,
            "lng": st.session_state.user_lng,
            "label": "You are here",
            "map_label": "",
            "detail": "Demo location: District 1",
            "price": "",
            "color": [246, 200, 95, 235],
            "radius": 95,
        }
    ]
    seen = set()
    pickup_number = 1
    for item in sorted_results:
        lat = item.get("lat")
        lng = item.get("lng")
        if lat is None or lng is None:
            continue
        key = (round(float(lat), 5), round(float(lng), 5), item.get("store_name"))
        if key in seen:
            continue
        seen.add(key)
        markers.append(
            {
                "lat": float(lat),
                "lng": float(lng),
                "label": f"{pickup_number}. {item.get('store_name', 'Rescue store')}",
                "map_label": str(pickup_number),
                "detail": f"{item.get('name', 'Rescue item')} - {item.get('distance_km', 0):.1f} km away",
                "price": vnd(item.get("price", 0)),
                "color": [31, 191, 117, 230],
                "radius": 110,
            }
        )
        pickup_number += 1
    return markers


def render_map_legend():
    st.markdown(
        """
<div class="map-legend">
    <span class="legend-item"><span class="legend-dot legend-user"></span>Your demo location</span>
    <span class="legend-item"><span class="legend-dot legend-store"></span>Numbered rescue pickup point</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_results_map(results):
    markers = map_marker_rows(results)
    if pdk is None:
        st.markdown(
            f"""
<div class="map-panel">
    <div>
        <div style="font-size:0.78rem; opacity:0.82; font-weight:700; text-transform:uppercase;">Nearby map</div>
        <div style="font-size:1.15rem; font-weight:800; margin-top:0.25rem;">District 1 pickup route</div>
    </div>
    <div style="font-size:0.86rem; opacity:0.9;">{max(0, len(markers) - 1)} numbered rescue stops sorted by distance.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        render_map_legend()
        return

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=markers,
        get_position="[lng, lat]",
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        auto_highlight=True,
    )
    number_layer = pdk.Layer(
        "TextLayer",
        data=markers,
        get_position="[lng, lat]",
        get_text="map_label",
        get_size=16,
        get_color=[255, 255, 255, 255],
        get_text_anchor="middle",
        get_alignment_baseline="center",
        font_weight=800,
    )
    deck = pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=st.session_state.user_lat,
            longitude=st.session_state.user_lng,
            zoom=13.4,
            pitch=0,
        ),
        layers=[layer, number_layer],
        tooltip={"html": "<b>{label}</b><br/>{detail}<br/>{price}", "style": {"fontSize": "12px"}},
    )
    st.pydeck_chart(deck, use_container_width=True)
    render_map_legend()

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
            render_quick_search_card(term)
            st.button(
                "Search",
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

    render_results_map(results)

    filtered = sorted(results, key=lambda item: item.get('distance_km', 0))

    if not filtered:
        st.info("No rescue food is available nearby yet. Try another search.")

    for index, item in enumerate(filtered):
        savings = max(0, int(item["original_price"] or 0) - int(item["price"] or 0))
        st.markdown(
            f"""
<div class="result-card">
    <div style="display:flex; gap:0.8rem; align-items:flex-start;">
        <div class="dish-image-wrap">
            <img class="dish-thumb" src="{dish_image_src(item)}" alt="{item['name']}" />
            <div class="dish-index">{index + 1}</div>
        </div>
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
    <div class="detail-photo"><img src="{dish_image_src(item)}" alt="{item['name']}" /></div>
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
        st.markdown(
            """
<div class="delivery-panel">
    <div class="result-title" style="font-size:0.98rem;">Choose delivery partner</div>
    <div class="result-meta">A nearby driver will be matched for this demo reservation.</div>
    <div class="delivery-provider-row">
        <div class="delivery-provider-card"><div class="delivery-provider-logo">G</div><div class="delivery-provider-name">Grab</div></div>
        <div class="delivery-provider-card"><div class="delivery-provider-logo">be</div><div class="delivery-provider-name">Be</div></div>
        <div class="delivery-provider-card"><div class="delivery-provider-logo">A</div><div class="delivery-provider-name">AhaMove</div></div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.radio("Delivery partner", ["Grab", "Be", "AhaMove"], key="delivery_provider", horizontal=True)
        st.session_state.payment_method = "Mock online payment"
    else:
        payment_options = ["Pay at counter", "Mock online payment"]
        st.radio("Payment method", payment_options, key="payment_method")
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
                "delivery_provider": st.session_state.delivery_provider if st.session_state.pickup_method.startswith("Mock delivery") else None,
                "total": total,
                "customer": "Demo customer",
            }
            if st.session_state.pickup_method.startswith("Mock delivery"):
                navigate("DeliveryTracking")
            else:
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
    <div class="review-row"><span class="review-label">Method</span><span class="review-value">{reservation['pickup_method']}</span></div>
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
# PAGE: DELIVERY TRACKING
# ============================================================
def page_delivery_tracking():
    reservation = st.session_state.active_reservation
    if not reservation:
        st.warning("No active reservation yet.")
        if st.button("Back to search", use_container_width=True):
            navigate("UserHome")
        return

    item = reservation["item"]
    provider = reservation.get("delivery_provider") or st.session_state.delivery_provider

    st.markdown(
        f"""
<div class="driver-hero-card">
    <div style="font-size:0.78rem; font-weight:800; opacity:0.9; text-transform:uppercase;">Delivery match</div>
    <h2>Waiting for {provider} driver...</h2>
    <div style="font-size:0.9rem; opacity:0.9; margin-top:0.55rem;">Your rescue order is held while we match a nearby driver.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="driver-waiting-panel">
    <div class="delivery-status" style="margin-top:0;">
        <div class="delivery-pulse"></div>
        <div>
            <div class="delivery-status-title">Finding the best driver nearby</div>
            <div class="delivery-status-copy">Estimated match: 2-4 minutes. Pickup window: {item['pickup_window']}.</div>
        </div>
    </div>
</div>
<div class="driver-route-card">
    <div class="result-title">{item['name']}</div>
    <div class="result-meta">{item['store_name']} - {item['store_address']}</div>
    <div class="review-row"><span class="review-label">Delivery partner</span><span class="review-value">{provider}</span></div>
    <div class="review-row"><span class="review-label">Payment</span><span class="review-value">{reservation['payment_method']}</span></div>
    <div class="review-row"><span class="review-label">Total</span><span class="review-value">{vnd(reservation['total'])}</span></div>
</div>
<div class="driver-route-card">
    <div class="driver-step-row">
        <div class="driver-step-dot">1</div>
        <div><div class="driver-step-title">Driver accepts order</div><div class="driver-step-copy">LoopBite is checking nearby delivery partners.</div></div>
    </div>
    <div class="driver-step-row">
        <div class="driver-step-dot">2</div>
        <div><div class="driver-step-title">Pickup at merchant</div><div class="driver-step-copy">Driver shows the pickup code to collect the rescue item.</div></div>
    </div>
    <div class="driver-step-row">
        <div class="driver-step-dot">3</div>
        <div><div class="driver-step-title">Deliver to customer</div><div class="driver-step-copy">The item goes straight from store counter to customer.</div></div>
    </div>
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
        ("Dashboard", "Home"),
        ("Create", "Create"),
        ("Published", "List"),
        ("Completed", "Done"),
        ("Profile", "Profile"),
    ]
    cols = st.columns(len(pages))
    for col, (name, label_text) in zip(cols, pages):
        with col:
            is_active = st.session_state.page == name
            label = f"**{label_text}**" if is_active else label_text
            if st.button(label, key=f"nav_{name}", use_container_width=True):
                navigate(name)

def page_dashboard():
    merchant = api.get_merchant(DEMO_MERCHANT_ID) or {}
    merchant_name = merchant.get("name", "LoopBite Merchant")

    foods = merchant_food_items()
    available_foods = [f for f in foods if (f.get("quantity") or 0) > 0]
    dashboard_foods = available_foods[:6]
    low_stock = sorted([f for f in dashboard_foods if (f.get("quantity") or 0) <= 3], key=lambda x: x.get("quantity") or 0)
    display_items = sum(min(int(f.get("quantity") or 0), 8) for f in dashboard_foods)
    display_value = sum(int(float(f.get("price") or 0)) * min(int(f.get("quantity") or 0), 8) for f in dashboard_foods)
    active_listing_count = len(dashboard_foods)
    low_stock_count = len(low_stock)
    if not API_OK:
        st.warning("Backend offline. Demo data and session-state listings are still available.")

    st.markdown(
        f"""
<div class="top-bar">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:0.875rem; opacity:0.9;">LoopBite Merchant Portal</div>
            <div style="font-size:1.25rem; font-weight:700;">{merchant_name}</div>
        </div>
        <div style="font-size:1.75rem; font-weight:800;">LB</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="dashboard-section-title">
    <h3>Today Overview</h3>
    <span class="badge badge-active">Demo ready</span>
</div>
<div class="dashboard-grid">
    <div class="dashboard-card primary">
        <div class="dashboard-label">Items ready</div>
        <div class="dashboard-value">{display_items}</div>
        <div class="dashboard-hint">Across {active_listing_count} active listings</div>
    </div>
    <div class="dashboard-card">
        <div class="dashboard-label">Potential rescue value</div>
        <div class="dashboard-value">{short_vnd(display_value)}</div>
        <div class="dashboard-hint">Same-day pickup window</div>
    </div>
    <div class="dashboard-card">
        <div class="dashboard-label">Reservations</div>
        <div class="dashboard-value">{1 if st.session_state.active_reservation else 0}</div>
        <div class="dashboard-hint">Waiting for handoff</div>
    </div>
    <div class="dashboard-card">
        <div class="dashboard-label">Needs attention</div>
        <div class="dashboard-value">{low_stock_count}</div>
        <div class="dashboard-hint">Low stock listings</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dashboard-section-title"><h3>New Reservation</h3></div>', unsafe_allow_html=True)
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
    st.markdown("### Active Listings")
    if not available_foods:
        st.info("No active listings yet. Use Create to add one.")
    else:
        for food in dashboard_foods[:5]:
            icon = category_icon(food.get("category", ""))
            remaining = api.time_until(food.get("expiry_time"))
            display_qty = min(int(food.get("quantity") or 0), 8)
            st.markdown(
                f"""
<div class="food-card">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="width:2.5rem; height:2.5rem; border-radius:10px; background:#E6F7EE; color:#007A2F; display:flex; align-items:center; justify-content:center; font-weight:800;">{icon}</div>
        <div style="flex:1;">
            <div style="font-weight:600;">{food.get('name', '-')}</div>
            <div style="font-size:0.8rem; color:#6B7280;">Qty: {display_qty} - {remaining}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{vnd(food.get('price', 0))}</div>
            <span class="badge badge-active" style="margin-top:0.25rem;">Active</span>
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown("### Low Stock Alert")
    if not low_stock:
        st.success("All listings have healthy stock")
    else:
        for food in low_stock[:3]:
            icon = category_icon(food.get("category", ""))
            remaining = api.time_until(food.get("expiry_time"))
            st.markdown(
                f"""
<div class="food-card" style="border-left: 4px solid #F4A261;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="width:2.3rem; height:2.3rem; border-radius:10px; background:#FFF7E0; color:#6B4B00; display:flex; align-items:center; justify-content:center; font-weight:800;">{icon}</div>
            <div>
                <div style="font-weight:600;">{food.get('name', '-')}</div>
                <div style="font-size:0.875rem; color:#6B7280;">{remaining}</div>
            </div>
        </div>
        <span class="badge badge-danger">{food.get('quantity', 0)} left</span>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    render_bottom_nav()

def page_post():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">Create Rescue Item</h2>
    <p style="margin:0.25rem 0 0 0; font-size:0.875rem; opacity:0.9;">
        Create a rescue listing in under 60 seconds.
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
        if st.button("Create Listing", type="primary", use_container_width=True):
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
                    st.success(f"Created via API: {result.get('name')}")
                else:
                    result = add_mock_listing(
                        payload,
                        original_price=int(original_price),
                        pickup_window=pickup_window,
                        quality_note=quality_note.strip(),
                    )
                    st.success(f"Created in demo mode: {result.get('name')}")

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
    <h2 style="margin:0; color:white;">Active Listings</h2>
</div>
""",
        unsafe_allow_html=True,
    )
    if not API_OK:
        st.warning("Backend offline. Showing demo listings if available.")

    foods = merchant_food_items()
    available = [f for f in foods if (f.get("quantity") or 0) > 0]
    listings = [
        {
            "id": f.get("id"),
            "name": f.get("name", "-"),
            "qty": f.get("quantity", 0),
            "price": vnd(f.get("price", 0)),
            "exp": api.time_until(f.get("expiry_time")),
            "status": "Active",
            "icon": category_icon(f.get("category", "")),
        }
        for f in available
    ]

    tabs = st.tabs([f"All ({len(listings)})", f"Active ({len(listings)})"])
    with tabs[0]:
        render_listings(listings, prefix="all")
    with tabs[1]:
        render_listings(listings, prefix="active")
    render_bottom_nav()


def render_listings(listings, prefix=""):
    if not listings:
        st.info("No listings yet. Use Create to add one.")
        return
    for item in listings:
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="width:2.5rem; height:2.5rem; border-radius:10px; background:#E6F7EE; color:#007A2F; display:flex; align-items:center; justify-content:center; font-weight:800;">{item['icon']}</div>
        <div style="flex:1;">
            <div style="font-weight:600;">{item['name']}</div>
            <div style="font-size:0.8rem; color:#6B7280;">Qty: {item['qty']} - {item['exp']}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{item['price']}</div>
            <span class="badge badge-active" style="margin-top:0.25rem;">{item['status']}</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

def page_completed():
    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">Completed Orders</h2>
</div>
""",
        unsafe_allow_html=True,
    )
    foods = merchant_food_items()
    sold = [f for f in foods if (f.get("quantity") or 0) == 0]
    reservation = st.session_state.active_reservation
    picked_up = [reservation] if reservation and reservation.get("status") == "Picked Up" else []
    total_revenue = sum((f.get("price") or 0) * 5 for f in sold) + sum(r.get("total", 0) for r in picked_up)
    total_items_sold = len(sold) * 5 + sum(r.get("quantity", 0) for r in picked_up)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Orders", str(len(sold) + len(picked_up)))
    with c2:
        st.metric("Items", str(total_items_sold))
    with c3:
        st.metric("Revenue", vnd(total_revenue))

    st.divider()
    if not sold and not picked_up:
        st.info("No completed orders yet.")
    for reservation in picked_up:
        item = reservation["item"]
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between; align-items:start;">
        <div>
            <div style="font-weight:600;">{item.get('name', '-')}</div>
            <div style="font-size:0.875rem; color:#6B7280;">Pickup code {reservation['pickup_code']}</div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">Qty {reservation['quantity']} - Picked Up</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{vnd(reservation['total'])}</div>
            <span class="badge badge-gray" style="margin-top:0.25rem;">Picked Up</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    for order in sold[:20]:
        st.markdown(
            f"""
<div class="food-card">
    <div style="display:flex; justify-content:space-between; align-items:start;">
        <div>
            <div style="font-weight:600;">{order.get('name', '-')}</div>
            <div style="font-size:0.875rem; color:#6B7280;">LoopBite Merchant</div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">{api.time_until(order.get('expiry_time'))}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:700; color:#00A040;">{vnd(order.get('price', 0))}</div>
            <span class="badge badge-gray" style="margin-top:0.25rem;">Sold</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    render_bottom_nav()

def page_profile():
    merchant = api.get_merchant(DEMO_MERCHANT_ID) or {}
    merchant_name = merchant.get("name", "LoopBite Merchant")
    merchant_addr = merchant.get("address", "District 1 pickup point")

    st.markdown(
        """
<div class="top-bar">
    <h2 style="margin:0; color:white;">Profile</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="food-card" style="text-align:center; padding:1.5rem;">
    <div style="font-size:3rem; font-weight:900; color:#007A2F;">LB</div>
    <div style="font-weight:700; font-size:1.25rem; margin-top:0.5rem;">{merchant_name}</div>
    <div style="font-size:0.875rem; color:#6B7280;">Merchant ID: FM-{DEMO_MERCHANT_ID:03d}</div>
    <div style="font-size:0.75rem; color:#9CA3AF; margin-top:0.25rem;">{merchant_addr or '-'}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    foods = merchant_food_items()
    total_listings = len(foods)
    total_qty = sum((f.get("quantity") or 0) for f in foods)

    st.markdown("### This Month")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Listings", str(total_listings))
        st.metric("Total Items", str(total_qty))
    with c2:
        st.metric("API Status", "Online" if API_OK else "Offline")
        st.metric("Backend", "127.0.0.1:8000")

    st.divider()

    menu = [
        ("Store", "Store Information"),
        ("Pin", "Locations (3)"),
        ("Pay", "Payout Settings"),
        ("Bell", "Notifications"),
        ("Help", "Help & Support"),
        ("Gear", "Settings"),
        ("Exit", "Logout"),
    ]

    for icon, label in menu:
        st.markdown(
            f"""
<div class="food-card" style="padding:0.75rem 1rem;">
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="width:2.25rem; color:#007A2F; font-weight:800;">{icon}</div>
        <div style="flex:1; font-weight:500;">{label}</div>
        <div style="color:#9CA3AF;">&gt;</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    render_bottom_nav()

# ============================================================
# ROUTER
# ============================================================
USER_ROUTES = {"UserHome", "UserResults", "FoodDetail", "ReservationReview", "PickupConfirmation", "DeliveryTracking"}
MERCHANT_ROUTES = {"Dashboard", "Create", "Published", "Completed", "Profile", "Post"}

ROUTES = {
    "UserHome": page_user_home,
    "UserResults": page_user_results,
    "FoodDetail": page_food_detail,
    "ReservationReview": page_reservation_review,
    "PickupConfirmation": page_pickup_confirmation,
    "DeliveryTracking": page_delivery_tracking,
    "Dashboard": page_dashboard,
    "Create": page_post,
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

render_app_switch()
page_fn = ROUTES.get(st.session_state.page, page_user_home)
page_fn()

