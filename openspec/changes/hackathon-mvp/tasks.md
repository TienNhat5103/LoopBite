## 1. Project Setup

- [ ] 1.1 Create or verify the React + Vite + TypeScript app structure.
- [ ] 1.2 Add Supabase client configuration using environment variables.
- [ ] 1.3 Add routing for `/`, `/item/:id`, `/checkout/:itemId`, `/receipt/:orderId`, and LoopBite Merchant listing/order surfaces.

## 2. Supabase Data Model

- [ ] 2.1 Create `merchants`, `listings`, and `orders` tables; add `profiles` only if Supabase Auth is introduced.
- [ ] 2.2 Add enums or equivalent constraints for `food_category`, `risk_group`, `listing_status`, `fulfillment_method`, `payment_method`, `payment_status`, and `order_status`.
- [ ] 2.3 Add merchant fields needed for pickup address, optional location, and seller profile display.
- [ ] 2.4 Add listing fields needed for low-risk rescue food details, prices, pickup window, best-before or consume-before timing, quality note, fulfillment options, payment options, and status.
- [ ] 2.5 Add order fields needed for reservation quantity, amount, fulfillment method, payment method, payment status, order status, and pickup code.
- [ ] 2.6 Configure minimum RLS policies or demo-safe access rules for public eligible listing reads, user order creation, merchant listing management, merchant order reads, and pickup confirmation.
- [ ] 2.7 Prepare demo data or a live demo path for target merchants and published low-risk listings.

## 3. User Flow

- [ ] 3.1 Build keyword search and geolocation request on `/`.
- [ ] 3.2 Build Map + List results using eligible published listings from Supabase.
- [ ] 3.3 Build item detail loading for `/item/:id`.
- [ ] 3.4 Add filters for food category, distance, price, pickup window, best-before or consume-before timing, and availability.
- [ ] 3.5 Add unavailable states for missing, sold-out, expired, unpublished, or high-risk listings.
- [ ] 3.6 Add checkout entry from eligible item detail to `/checkout/:itemId`.

## 4. Order Flow

- [ ] 4.1 Create checkout selection for `fulfillment_method` and `payment_method` without collecting real payment details.
- [ ] 4.2 Insert the `orders` row in Supabase, generate `pickup_code`, calculate `amount`, and set `order_status = reserved`.
- [ ] 4.3 Redirect successful mock orders to `/receipt/:orderId`.
- [ ] 4.4 Build the receipt page with pickup code, pickup time, merchant address, amount, and order status.
- [ ] 4.5 Add a not-found or unavailable state for missing receipts.

## 5. Merchant Flow

- [ ] 5.1 Build My Listings to show only the current merchant's listings.
- [ ] 5.2 Show item name, food category, status, rescue price, quantity, pickup window, and order count for each listing.
- [ ] 5.3 Add the empty state and "Post rescue item" action.
- [ ] 5.4 Build the post rescue item form with required listing fields.
- [ ] 5.5 Publish new low-risk listings to Supabase owned by the merchant.
- [ ] 5.6 Show reserved orders for the merchant's listings.
- [ ] 5.7 Add pickup-code confirmation to update `order_status = picked_up`.
- [ ] 5.8 Decrease listing quantity after pickup and set listing `status = sold_out` when quantity reaches zero.
- [ ] 5.9 Verify eligible published listings appear in the user app.

## 6. Demo Verification

- [ ] 6.1 Verify the merchant can create and publish a low-risk rescue food listing.
- [ ] 6.2 Verify the user can search, view Map + List results, open item detail, reserve an item, and view a receipt.
- [ ] 6.3 Verify the merchant can see the reserved order and confirm pickup with the pickup code.
- [ ] 6.4 Verify quantity decreases after pickup and sold-out listings stop appearing as orderable.
- [ ] 6.5 Verify no FastAPI, real payment, real delivery integration, Grab/Ahamove integration, admin dashboard, impact dashboard, analytics, recommendation engine, or high-risk food category was added.
