# LoopBite MVP Architecture

## 1. Architecture Overview

The MVP is a browser-based React application backed directly by Supabase. The frontend uses the Supabase client to read and write merchant, listing, and order data through Supabase's auto-generated API.

There is no custom backend service in the MVP. Supabase provides the database, API layer, row-level security, and seed data needed for the hackathon demo.

## 2. Text Diagram

```text
Browser -> React App -> Supabase Client -> Supabase Postgres + RLS
```

## 3. Frontend Responsibilities

- Show keyword search, geolocation request, and nearby rescue food Map + List results on `/`.
- Show rescue food item details on `/item/:id`.
- Validate checkout and submit mock reservations on `/checkout/:itemId`.
- Show receipts on `/receipt/:orderId`.
- Provide LoopBite Merchant listing screens.
- Show merchant listing order counts and active reservations.
- Confirm pickup with a pickup code.
- Handle loading, empty, validation, and insert failure states.

## 4. Supabase Responsibilities

- Store MVP data in Postgres tables.
- Expose auto-generated API access through the Supabase client.
- Enforce row-level security policies.
- Provide seed data for demo merchants and low-risk rescue food listings.
- Persist mock order reservations and pickup confirmation state.

## 5. User Data Flow

1. Browser loads the React app.
2. React app requests geolocation after keyword search.
3. React app fetches eligible published listings joined with merchant pickup data from Supabase.
4. User opens an item detail page at `/item/:id`.
5. React app fetches the selected eligible listing from Supabase.
6. User chooses fulfillment and payment options in checkout.
7. React app creates an `orders` row with `order_status = reserved` and a `pickup_code`.
8. React app redirects to the receipt page and fetches order, listing, and merchant receipt data.

## 6. Merchant Data Flow

1. Merchant opens LoopBite Merchant.
2. React app fetches the merchant's listings and simple order counts.
3. Merchant opens the post rescue item form.
4. Merchant creates or edits low-risk listing data.
5. React app writes the listing to Supabase.
6. Merchant publishes the listing.
7. Eligible published listings become visible to users.
8. Merchant opens reserved orders, checks the user's `pickup_code`, and confirms pickup.
9. Supabase updates `order_status = picked_up`, decreases listing quantity, and marks the listing `sold_out` when quantity reaches zero.

## 7. Why FastAPI Is Excluded

FastAPI is excluded from the MVP to reduce setup, deployment, and integration work during the hackathon. Supabase already provides the API, database, and access-control layer needed for the demo scope.

A separate backend would add value later for payments, external integrations, complex authorization, analytics jobs, and server-only workflows, but those are outside the MVP.

## 8. Future Architecture

- **Auth**: Add Supabase Auth for user and merchant accounts.
- **Payment**: Add a real payment provider and server-side payment verification.
- **Delivery integration**: Add real delivery providers only outside MVP scope.
- **Merchant integration**: Sync orders, merchants, and listing availability with external systems.
- **Analytics**: Add reporting pipelines, impact dashboards, and operational metrics.
- **Server-side functions**: Add Supabase Edge Functions or a dedicated backend for trusted business logic, webhooks, and scheduled jobs.
