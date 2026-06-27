# MVP Database Design

## 1. Database Overview

The MVP uses Supabase Postgres as the only backend data store and API source. The demo relies on curated seed data for merchants and campaigns, while `orders` and `impact_events` are created live during the demo.

There is no FastAPI service, admin dashboard, impact dashboard, or real payment data in the MVP database.

## 2. Tables and Key Fields

### merchants

- `id`: Primary key.
- `name`: Merchant display name.
- `description`: Short merchant summary.
- `logo_url`: Optional merchant logo.
- `created_at`: Creation timestamp.

### campaigns

- `id`: Primary key.
- `merchant_id`: Foreign key to `merchants.id`.
- `title`: Campaign name.
- `description`: Campaign details.
- `image_url`: Optional campaign image.
- `original_price`: Reference price before discount.
- `discounted_price`: Demo purchase price.
- `donation_rate`: Percentage of discounted price used for impact.
- `is_published`: Controls public visibility.
- `created_at`: Creation timestamp.

### orders

- `id`: Primary key.
- `campaign_id`: Foreign key to `campaigns.id`.
- `quantity`: Mock order quantity.
- `unit_price`: Price copied from the campaign at order time.
- `total_amount`: `quantity * unit_price`.
- `created_at`: Creation timestamp.

### impact_events

- `id`: Primary key.
- `order_id`: Unique foreign key to `orders.id`.
- `campaign_id`: Foreign key to `campaigns.id`.
- `donation_amount`: Calculated donation amount for the order.
- `description`: Human-readable impact summary.
- `created_at`: Creation timestamp.

## 3. Optional Future Table

### profiles

Add `profiles` only if Supabase Auth is introduced later.

- `id`: Primary key matching `auth.users.id`.
- `role`: User role, such as `user` or `merchant`.
- `merchant_id`: Optional link to `merchants.id`.
- `created_at`: Creation timestamp.

## 4. Relationships

- `merchants` 1-* `campaigns`
- `campaigns` 1-* `orders`
- `orders` 1-1 `impact_events`
- `campaigns` 1-* `impact_events`

## 5. RLS Plan

### Demo-Friendly Policies

- Allow public read access to published campaigns and merchant details.
- Allow inserting mock orders for published campaigns.
- Allow inserting impact events linked to newly created orders.
- Allow merchant campaign CRUD without production-grade authentication for demo speed.

### Future Production Policies

- Require Supabase Auth for all writes.
- Restrict merchant campaign writes to authenticated owners.
- Restrict order and receipt reads to the owning user or merchant.
- Validate server-side impact event creation through trusted functions.
- Separate public campaign access from private merchant operations.

## 6. Seed Data Plan

- Create 2 merchants.
- Create 4-6 campaigns across those merchants.
- Include only published demo campaigns needed for the user flow.
- Include optional unpublished campaigns for edge-case testing.
- Do not seed admin data.
- Do not seed dashboard data.
- Create orders and impact events live during the demo instead of seeding them.

## 7. Impact Formula

```text
donation_amount = discounted_price * donation_rate / 100
```

For multi-quantity orders, calculate the order-level donation from the total discounted amount:

```text
donation_amount = quantity * discounted_price * donation_rate / 100
```

## 8. Expected SQL Files

- `supabase/migrations/001_initial_schema.sql`
- `supabase/seed.sql`
