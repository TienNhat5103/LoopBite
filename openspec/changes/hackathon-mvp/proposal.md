## Why

Build a demo-stable hackathon MVP that shows the full loop between users and merchants: merchants publish impact-driven campaigns, users support them through a mock order, and users receive a simple impact receipt.

## What Changes

- Add a public campaign browsing flow with campaign cards and campaign detail pages.
- Add a mock support/order flow that creates an order and impact event in Supabase.
- Add a receipt flow showing campaign, merchant, amount, impact message, and thank-you message.
- Add a merchant flow for creating, publishing, and viewing own campaigns with simple order counts.
- Use Supabase for database, auth if needed, and API access.
- Do not add FastAPI, real payment, Grab integration, admin dashboards, analytics, recommendations, or inventory sync.

## Capabilities

### New Capabilities

- `user-flow`: User browsing and campaign detail experience.
- `merchant-flow`: Merchant campaign creation, publishing, listing, and order count experience.
- `order-flow`: Mock order creation, impact event creation, and receipt experience.

### Modified Capabilities

- None.

## Impact

- Frontend routes: `/`, `/campaign/:id`, `/receipt/:orderId`, `/merchant`, `/merchant/campaigns/new`.
- Supabase tables: `profiles`, `merchants`, `campaigns`, `orders`, `impact_events`.
- Supabase RLS policies for public campaign reads, user order creation, merchant campaign management, and merchant order visibility.
