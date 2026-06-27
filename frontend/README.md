# FamilyMart Rescue - Merchant Dashboard

Mobile-first Streamlit UI for FamilyMart merchants to manage food rescue listings.

## Features

- Dashboard with today's stats (rescued items, revenue, active listings)
- New reservation requests (accept/decline)
- Post rescue food items with photos and discount calculation
- Active listings management (pending / confirmed)
- Reservation details with customer info
- Completed orders history
- Store profile with monthly metrics

## Quick Start

```bash
cd d:/HACKATHON/merchant-ui
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 on your phone or browser.

For mobile view: open browser DevTools → toggle device toolbar → iPhone.

## Pages

| Page | Purpose |
|------|---------|
| Dashboard | Today's overview + new requests |
| Post | Create new rescue food listing |
| Published | Active listings (pending/confirmed) |
| Reservation | Order detail view |
| Completed | Order history |
| Profile | Store info + stats |

## Design

- Mobile-first responsive (max-width 480px)
- FamilyMart brand colors (#00A040 green)
- Card-based layout
- Bottom navigation (5 tabs)
- Custom CSS for native app feel
