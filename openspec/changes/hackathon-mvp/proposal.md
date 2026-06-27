## Why

Build a demo-stable LoopBite hackathon MVP that shows the full loop between users and merchants: merchants publish low-risk rescue food listings, users reserve affordable nearby items, and merchants confirm pickup with a pickup code.

## What Changes

- Add a public LoopBite user flow for keyword search, geolocation, nearby rescue food Map + List results, item detail, checkout, and receipt.
- Add a LoopBite Merchant flow for My Listings, posting low-risk rescue items, publishing listings, seeing reserved orders, and confirming pickup.
- Finalize the Supabase database contract for both apps around `merchants`, `listings`, and `orders`.
- Limit MVP food scope to low-risk / quality-based categories only.
- Keep payment and delivery mock-only.
- Do not add FastAPI, real payment, real delivery integration, Grab/Ahamove integration, admin dashboards, impact dashboards, analytics, recommendations, or high-risk food categories.

## Capabilities

### New Capabilities

- `user-flow`: User search, nearby rescue food discovery, item detail, and checkout entry experience.
- `merchant-flow`: Merchant listing creation, publishing, order visibility, and pickup confirmation experience.
- `order-flow`: Reservation creation, pickup code generation, receipt, and pickup completion experience.
- `database`: Shared Supabase data contract for the user app and merchant app.

### Modified Capabilities

- None.

## Impact

- Frontend routes: `/`, `/item/:id`, `/checkout/:itemId`, `/receipt/:orderId`, plus LoopBite Merchant listing and order-management surfaces.
- Supabase tables: `merchants`, `listings`, and `orders`; optional `profiles` only if Supabase Auth is introduced.
- Supabase policies or demo access rules for public eligible listing reads, user order creation, merchant listing management, merchant order visibility, and pickup confirmation.
