# MVP Architecture

## 1. Architecture Overview

The MVP is a browser-based React application backed directly by Supabase. The frontend uses the Supabase client to read and write campaign, order, merchant, and impact data through Supabase's auto-generated API.

There is no custom backend service in the MVP. Supabase provides the database, API layer, row-level security, and seed data needed for the hackathon demo.

## 2. Text Diagram

```text
Browser -> React App -> Supabase Client -> Supabase Postgres + RLS
```

## 3. Frontend Responsibilities

- Show the campaign list on `/`.
- Show campaign details on `/campaign/:id`.
- Validate and submit mock orders.
- Show receipts on `/receipt/:orderId`.
- Provide merchant campaign CRUD screens.
- Show simple merchant campaign lists and order counts.
- Handle loading, empty, validation, and insert failure states.

## 4. Supabase Responsibilities

- Store MVP data in Postgres tables.
- Expose auto-generated API access through the Supabase client.
- Enforce row-level security policies.
- Provide seed data for demo campaigns, merchants, orders, and impact events.
- Persist mock orders and linked impact events.

## 5. User Data Flow

1. Browser loads the React app.
2. React app fetches published campaigns from Supabase.
3. User opens a campaign detail page.
4. React app fetches the selected campaign from Supabase.
5. User submits a mock order.
6. React app creates an `orders` row.
7. React app creates a linked `impact_events` row.
8. React app redirects to the receipt page and fetches receipt data.

## 6. Merchant Data Flow

1. Merchant opens `/merchant`.
2. React app fetches merchant campaigns and simple order counts.
3. Merchant opens `/merchant/campaigns/new`.
4. Merchant creates or edits campaign data.
5. React app writes the campaign to Supabase.
6. Merchant publishes the campaign.
7. Published campaigns become visible to users.

## 7. Why FastAPI Is Excluded

FastAPI is excluded from the MVP to reduce setup, deployment, and integration work during the hackathon. Supabase already provides the API, database, and access-control layer needed for the demo scope.

A separate backend would add value later for payments, external integrations, complex authorization, analytics jobs, and server-only workflows, but those are outside the MVP.

## 8. Future Architecture

- **Auth**: Add Supabase Auth for user and merchant accounts.
- **Payment**: Add a real payment provider and server-side payment verification.
- **Grab/merchant integration**: Sync orders, merchants, and campaign availability with external systems.
- **Analytics**: Add reporting pipelines, impact dashboards, and operational metrics.
- **Server-side functions**: Add Supabase Edge Functions or a dedicated backend for trusted business logic, webhooks, and scheduled jobs.
