PRODUCT BRIEF FOR OPENSPEC

Project:
We are building a hackathon MVP for a two-sided web platform connecting users and merchants through impact-driven campaigns/listings.

Core idea:
Merchants can publish discounted or impact-driven campaigns.
Users can browse campaigns, support/buy/reserve a campaign through a mock order, and receive a simple receipt showing their contribution/impact.

Hackathon constraint:
This must be demo-stable and buildable fast. Prioritize clear user flow and merchant flow over complex architecture.

Stack:
- Frontend: React + Vite + TypeScript
- Backend/API: Supabase only
- Database: Supabase Postgres
- Auth: Supabase Auth if needed
- Do NOT use FastAPI

Actors:
1. User
   - Browses campaigns
   - Opens campaign detail
   - Creates a mock support/order action
   - Receives a confirmation/impact receipt

2. Merchant
   - Creates a campaign/listing
   - Publishes campaign
   - Views own campaigns
   - Sees simple order count for each campaign

User Flow:
1. User opens landing page `/`
2. User sees campaign cards
3. User clicks a campaign
4. User opens `/campaign/:id`
5. User reviews campaign details
6. User clicks "Support / Buy / Reserve"
7. User confirms mock order
8. System creates order in Supabase
9. System creates impact event in Supabase
10. User is redirected to `/receipt/:orderId`
11. User sees campaign name, merchant name, order amount, donation/impact message, and thank-you message

Merchant Flow:
1. Merchant opens `/merchant`
2. Merchant sees own campaign list
3. Merchant clicks "Create campaign"
4. Merchant opens `/merchant/campaigns/new`
5. Merchant enters campaign information:
   - title
   - description
   - original price
   - discounted price
   - quantity
   - donation rate or impact message
   - optional image URL
6. Merchant publishes campaign
7. Campaign appears on user landing page
8. Merchant can return to `/merchant` and see simple order count per campaign

Routes:
- `/`
- `/campaign/:id`
- `/receipt/:orderId`
- `/merchant`
- `/merchant/campaigns/new`

Supabase tables:
- profiles
- merchants
- campaigns
- orders
- impact_events

Minimum RLS rules:
- Public can read published campaigns
- Authenticated users can create their own mock orders
- Merchants can manage their own campaigns
- Merchants can read orders related to their own campaigns

Explicit non-goals:
- No FastAPI
- No Impact Dashboard
- No Admin Dashboard
- No Admin seed demo
- No real payment
- No real Grab integration
- No complex analytics
- No recommendation engine
- No inventory synchronization