# LoopBite MVP Database Design

## 1. Database Overview

The MVP uses Supabase Postgres as the only backend data store and API source. The demo relies on curated seed data for merchants and low-risk rescue food listings, while `orders` are created live during the demo.

There is no FastAPI service, admin dashboard, impact dashboard, or real payment data in the MVP database.

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
- `logo_url`: Optional merchant logo.
- `created_at`: Creation timestamp.

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

## 5. Visibility and Reservation Rules

- A listing appears in the user app only when `status = published`, `quantity > 0`, the pickup window is still valid, and `risk_group = low_risk_quality_based`.
- Listing `food_category` must be one of `bakery`, `packaged_food`, `dry_noodles`, `cereal`, `snack`, `sealed_drink`, or `other_low_risk`.
- High-risk fresh cooked meals, raw meat, seafood, dairy-heavy items, and unsafe perishables are not valid MVP listing categories.
- Creating an order reserves quantity and generates a `pickup_code`.
- Confirming pickup sets `order_status = picked_up`.
- Confirmed pickup decreases listing quantity.
- If listing quantity reaches zero, listing status becomes `sold_out`.

## 6. Optional Future Table

### profiles

Add `profiles` only if Supabase Auth is introduced later.

- `id`: Primary key matching `auth.users.id`.
- `role`: User role, such as `user` or `merchant`.
- `merchant_id`: Optional link to `merchants.id`.
- `created_at`: Creation timestamp.

## 7. Relationships

- `merchants` 1-* `listings`
- `listings` 1-* `orders`

## 8. RLS Plan

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

## 9. Seed Data Plan

- Create 2-3 merchants across bakeries, convenience stores, mini supermarkets, or small shops.
- Create 4-6 low-risk listings across those merchants.
- Include only published demo listings that satisfy quantity, pickup window, and low-risk category rules for the user flow.
- Include optional draft, sold-out, or expired listings for edge-case testing.
- Do not seed admin data.
- Do not seed dashboard data.
- Create orders live during the demo instead of seeding them.

## 10. Amount Formula

```text
amount = quantity * rescue_price
```

## 11. Expected SQL Files

- `supabase/migrations/001_initial_schema.sql`
- `supabase/seed.sql`
