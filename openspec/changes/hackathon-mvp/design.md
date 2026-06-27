## Context

This MVP is a two-sided React + Vite + TypeScript web app backed only by Supabase. The demo must clearly show public campaign discovery, mock user support, receipt confirmation, and merchant campaign publishing without complex integrations.

## Goals / Non-Goals

**Goals:**

- Ship the required five routes with a simple, reliable happy path.
- Store merchants, campaigns, orders, and impact events in Supabase Postgres.
- Use Supabase RLS to protect merchant-owned data and user-created orders.
- Keep the UI demo-friendly with clear empty, loading, error, and success states. 

**Non-Goals:**

- No FastAPI or separate backend service.
- No real payment, real Grab integration, admin dashboard, impact dashboard, analytics, recommendation engine, or inventory synchronization.
- No complex merchant onboarding beyond what is needed for the demo.

## Decisions

- Use Supabase client calls directly from the frontend.
  - Rationale: fastest path for a hackathon MVP and matches the brief.
  - Alternative considered: custom API server. Rejected because FastAPI and separate backend work are explicit non-goals.
- Model campaigns as the main public listing entity with a `published` status.
  - Rationale: public users only need published campaigns, while merchants need to manage their own campaign records.
  - Alternative considered: separate draft and published tables. Rejected as unnecessary for the demo.
- Create an `orders` row and an `impact_events` row during mock confirmation.
  - Rationale: makes the receipt and contribution message concrete without real payment processing.
  - Alternative considered: receipt-only local state. Rejected because Supabase persistence is required by the brief.
- Show simple aggregate order counts on the merchant campaign list.
  - Rationale: satisfies merchant visibility without adding analytics.
  - Alternative considered: detailed reporting dashboard. Rejected as an explicit non-goal.

## Risks / Trade-offs

- Auth setup may slow the demo -> use the simplest Supabase Auth path needed for merchant ownership and user order ownership.
- Direct frontend writes rely on correct RLS -> keep policies minimal and test each actor path manually.
- Mock orders can oversell campaign quantity -> show quantity for context but avoid inventory synchronization logic beyond creating the mock order.
- Optional image URLs can break visually -> use a stable fallback campaign image/card state when no usable URL is present.

## Migration Plan

1. Create Supabase tables and RLS policies.
2. Seed or create at least one merchant and published campaign for the demo.
3. Build the routes and connect them to Supabase.
4. Verify the happy path: merchant publishes campaign, user supports campaign, receipt renders.

Rollback is to remove the MVP routes/components and drop the demo Supabase tables or policies if they are no longer needed.

## Open Questions

- Which Supabase Auth method will be used during the demo for user and merchant identities?
- Will demo data be pre-seeded, entered live through the merchant form, or both?
