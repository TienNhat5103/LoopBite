## 1. Project Setup

- [ ] 1.1 Create or verify the React + Vite + TypeScript app structure.
- [ ] 1.2 Add Supabase client configuration using environment variables.
- [ ] 1.3 Add routing for `/`, `/campaign/:id`, `/receipt/:orderId`, `/merchant`, and `/merchant/campaigns/new`.

## 2. Supabase Data Model

- [ ] 2.1 Create `profiles`, `merchants`, `campaigns`, `orders`, and `impact_events` tables.
- [ ] 2.2 Add fields needed for campaign title, description, prices, quantity, publish status, impact message, optional image URL, and ownership.
- [ ] 2.3 Add fields needed for mock orders and linked impact events.
- [ ] 2.4 Configure minimum RLS policies for public campaign reads, user order creation, merchant campaign management, and merchant order reads.
- [ ] 2.5 Prepare demo data or a live demo path for at least one merchant and published campaign.

## 3. User Flow

- [ ] 3.1 Build the landing page campaign card list using published campaigns from Supabase.
- [ ] 3.2 Build campaign detail loading for `/campaign/:id`.
- [ ] 3.3 Add unavailable states for missing or unpublished campaigns.
- [ ] 3.4 Add a support, buy, or reserve action that opens the mock order confirmation path.

## 4. Order Flow

- [ ] 4.1 Create the mock order confirmation logic without collecting payment details.
- [ ] 4.2 Insert the `orders` row and linked `impact_events` row in Supabase.
- [ ] 4.3 Redirect successful mock orders to `/receipt/:orderId`.
- [ ] 4.4 Build the receipt page with campaign name, merchant name, amount, impact message, and thank-you message.
- [ ] 4.5 Add a not-found or unavailable state for missing receipts.

## 5. Merchant Flow

- [ ] 5.1 Build `/merchant` to show only the current merchant's campaigns.
- [ ] 5.2 Show title, status, discounted price, quantity, and simple order count for each campaign.
- [ ] 5.3 Add the empty state and create campaign action.
- [ ] 5.4 Build `/merchant/campaigns/new` with the required campaign fields.
- [ ] 5.5 Publish new campaigns to Supabase owned by the merchant.
- [ ] 5.6 Verify published campaigns appear on the public landing page.

## 6. Demo Verification

- [ ] 6.1 Verify the merchant can create and publish a campaign.
- [ ] 6.2 Verify the user can browse campaigns, open detail, confirm a mock order, and view a receipt.
- [ ] 6.3 Verify merchant order counts update after mock orders.
- [ ] 6.4 Verify no FastAPI, real payment, admin dashboard, impact dashboard, analytics, recommendation engine, Grab integration, or inventory sync was added.
