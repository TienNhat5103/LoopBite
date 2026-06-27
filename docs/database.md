# LoopBite MVP Database Design

## 1. Database Overview

The MVP uses Supabase Postgres as the only backend data store and API source for both the LoopBite user app and LoopBite Merchant app. The demo relies on curated seed data for merchants and low-risk rescue food listings, while `orders` are created live during the demo.

There is no FastAPI service, admin dashboard, impact dashboard, or real payment data in the MVP database.

The finalized MVP data model is:

- `merchants`: Pickup locations and seller profile data.
- `listings`: Merchant-posted low-risk rescue food inventory.
- `orders`: User reservations and merchant pickup confirmation state.

`profiles` is optional and should only be added if Supabase Auth is introduced during implementation.

## 2. Food Scope Constraints

Merchants can only post low-risk, quality-based food items:

- bread
- dry bakery items
- packaged food
- cereal
- dry noodles
- snacks
- sealed drinks
- similar low-risk items

The MVP avoids high-risk fresh cooked meals, raw meat, seafood, dairy-heavy items, and unsafe perishables.

## 3. Enums

### food_category

- `bakery`
- `packaged_food`
- `dry_noodles`
- `cereal`
- `snack`
- `sealed_drink`
- `other_low_risk`

### risk_group

- `low_risk_quality_based`

### listing_status

- `draft`
- `published`
- `sold_out`
- `expired`
- `cancelled`

### fulfillment_method

- `pickup`
- `delivery_mock`

### payment_method

- `pay_at_counter`
- `pay_online_mock`

### payment_status

- `unpaid`
- `mock_paid`
- `paid_at_counter`

### order_status

- `reserved`
- `picked_up`
- `cancelled`
- `expired`

## 4. Tables and Key Fields

### merchants

- `id`: Primary key.
- `name`: Merchant display name.
- `merchant_type`: Merchant type such as mini supermarket, bakery, convenience store, or small shop.
- `description`: Short merchant summary.
- `address`: Merchant pickup address.
- `latitude`: Optional pickup latitude for nearby search and Map view.
- `longitude`: Optional pickup longitude for nearby search and Map view.
- `logo_url`: Optional merchant logo.
- `created_at`: Creation timestamp.
- `updated_at`: Last update timestamp.

### listings

- `id`: Primary key.
- `merchant_id`: Foreign key to `merchants.id`.
- `item_name`: Rescue food item name.
- `image_url`: Item image URL.
- `food_category`: One of the supported low-risk food category enum values.
- `risk_group`: Defaults to `low_risk_quality_based`.
- `quantity`: Current quantity left.
- `original_price`: Reference price before discount.
- `rescue_price`: Discounted rescue price.
- `pickup_start_time`: Start of pickup window.
- `pickup_end_time`: End of pickup window.
- `best_before`: Optional best-before date/time.
- `consume_before`: Optional consume-before date/time.
- `quality_note`: Short quality condition note shown to users.
- `merchant_note`: Optional merchant-facing or pickup instruction note.
- `fulfillment_options`: Supported options such as `pickup` and optional `delivery_mock`.
- `payment_options`: Supported options such as `pay_at_counter` and `pay_online_mock`.
- `status`: Listing status such as `draft`, `published`, `sold_out`, `expired`, or `cancelled`.
- `created_at`: Creation timestamp.
- `updated_at`: Last update timestamp.

### orders

- `id`: Primary key.
- `listing_id`: Foreign key to `listings.id`.
- `quantity`: Reserved quantity.
- `amount`: Total order amount copied from listing price at order time.
- `fulfillment_method`: `pickup` or `delivery_mock`.
- `payment_method`: `pay_at_counter` or `pay_online_mock`.
- `payment_status`: Mock or offline payment state.
- `order_status`: `reserved`, `picked_up`, `cancelled`, or `expired`.
- `pickup_code`: Short code shown to the user and verified by the merchant at pickup.
- `created_at`: Creation timestamp.
- `updated_at`: Last update timestamp.

## 5. Field Constraints

### merchants

- `name` is required.
- `merchant_type` is required and must represent a target merchant type: mini supermarket, bakery, convenience store, or small shop.
- `address` is required for receipt and pickup instructions.
- `latitude` and `longitude` are optional for MVP but required for distance sorting and Map positioning.

### listings

- `merchant_id`, `item_name`, `food_category`, `risk_group`, `quantity`, `original_price`, `rescue_price`, `pickup_start_time`, `pickup_end_time`, `quality_note`, and `status` are required.
- `risk_group` defaults to `low_risk_quality_based`.
- `quantity` must be greater than or equal to 0.
- `original_price` and `rescue_price` must be greater than or equal to 0.
- `rescue_price` should be less than or equal to `original_price`.
- `pickup_end_time` must be later than `pickup_start_time`.
- At least one of `best_before` or `consume_before` should be present for user-facing quality guidance.
- `fulfillment_options` must include `pickup`; `delivery_mock` is optional only if time allows.
- `payment_options` must include `pay_at_counter`; `pay_online_mock` is optional.

### orders

- `listing_id`, `quantity`, `amount`, `fulfillment_method`, `payment_method`, `payment_status`, `order_status`, and `pickup_code` are required.
- `quantity` must be greater than 0.
- `amount` is calculated at reservation time from listing `rescue_price`.
- `pickup_code` must be generated when an order is created and must not be empty.
- New user reservations start with `order_status = reserved`.
- `pay_at_counter` starts with `payment_status = unpaid`.
- `pay_online_mock` may use `payment_status = mock_paid`.

## 6. User App Database Contract

The user app reads only eligible public listings and merchant pickup data needed for discovery, item detail, checkout, and receipt.

### User App Reads

- Search and Map + List view reads `listings` joined with `merchants`.
- Item detail reads one eligible `listings` row joined with its `merchants` row.
- Receipt reads one `orders` row joined with `listings` and `merchants`.

### User App Writes

- Checkout inserts an `orders` row for an eligible listing.
- Checkout reserves quantity logically at order creation time.
- The user app does not update merchant listing content.
- The user app does not mark orders as `picked_up`.

## 7. Merchant App Database Contract

The merchant app owns listing management and pickup completion for its own listings.

### Merchant App Reads

- My Listings reads `listings` filtered by `merchant_id`.
- Listing order views read `orders` joined with `listings` filtered by the merchant's own listings.

### Merchant App Writes

- Post rescue item inserts a `listings` row.
- Publish listing sets `status = published` only for valid low-risk listings.
- Merchant listing edits update only the merchant's own `listings`.
- Confirm pickup verifies `pickup_code`, sets `order_status = picked_up`, decreases listing `quantity`, and sets listing `status = sold_out` when quantity reaches 0.

## 8. Visibility and Reservation Rules

- A listing appears in the user app only when `status = published`, `quantity > 0`, the pickup window is still valid, and `risk_group = low_risk_quality_based`.
- Listing `food_category` must be one of `bakery`, `packaged_food`, `dry_noodles`, `cereal`, `snack`, `sealed_drink`, or `other_low_risk`.
- High-risk fresh cooked meals, raw meat, seafood, dairy-heavy items, and unsafe perishables are not valid MVP listing categories.
- Creating an order reserves quantity and generates a `pickup_code`.
- Confirming pickup sets `order_status = picked_up`.
- Confirmed pickup decreases listing quantity.
- If listing quantity reaches zero, listing status becomes `sold_out`.

## 9. Recommended Views or Query Shapes

### public_rescue_listings

Use a view or shared query shape for the user app that returns only eligible public listings:

- `listing_id`
- `merchant_id`
- `merchant_name`
- `merchant_address`
- `latitude`
- `longitude`
- `item_name`
- `image_url`
- `food_category`
- `risk_group`
- `quantity`
- `original_price`
- `rescue_price`
- `pickup_start_time`
- `pickup_end_time`
- `best_before`
- `consume_before`
- `quality_note`
- `fulfillment_options`
- `payment_options`
- `status`

### merchant_listing_orders

Use a view or shared query shape for the merchant app that returns a merchant's listings with order counts and active reservations:

- listing fields needed for My Listings
- `reserved_order_count`
- `picked_up_order_count`
- latest reserved order details when needed for pickup handling

## 10. Indexes

- `listings(merchant_id)` for My Listings.
- `listings(status, food_category)` for public filtering.
- `listings(pickup_start_time, pickup_end_time)` for pickup-window filtering.
- `listings(rescue_price)` for price filtering.
- `orders(listing_id)` for merchant order lookup.
- `orders(order_status)` for active reservation lookup.
- `orders(pickup_code)` for pickup confirmation lookup.

## 11. Optional Future Table

### profiles

Add `profiles` only if Supabase Auth is introduced later.

- `id`: Primary key matching `auth.users.id`.
- `role`: User role, such as `user` or `merchant`.
- `merchant_id`: Optional link to `merchants.id`.
- `created_at`: Creation timestamp.

## 12. Relationships

- `merchants` 1-* `listings`
- `listings` 1-* `orders`

## 13. RLS Plan

### Demo-Friendly Policies

- Allow public read access to eligible published listings and merchant details.
- Allow inserting mock orders for eligible published listings.
- Allow merchant listing CRUD without production-grade authentication for demo speed.
- Allow merchants to read orders linked to their own listings.
- Allow merchants to update an order to `picked_up` only after checking the pickup code.

### Future Production Policies

- Require Supabase Auth for all writes.
- Restrict merchant listing writes to authenticated owners.
- Restrict order and receipt reads to the owning user or merchant.
- Validate pickup confirmation and quantity updates through trusted server-side functions.
- Separate public listing access from private merchant operations.

## 14. Seed Data Plan

- Create 2-3 merchants across bakeries, convenience stores, mini supermarkets, or small shops.
- Create 4-6 low-risk listings across those merchants.
- Include only published demo listings that satisfy quantity, pickup window, and low-risk category rules for the user flow.
- Include optional draft, sold-out, or expired listings for edge-case testing.
- Do not seed admin data.
- Do not seed dashboard data.
- Create orders live during the demo instead of seeding them.

## 15. Amount Formula

```text
amount = quantity * rescue_price
```

## 16. Expected SQL Files

- `supabase/migrations/001_initial_schema.sql`
- `supabase/seed.sql`
