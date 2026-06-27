## Context

This MVP is a two-sided React + Vite + TypeScript web app backed only by Supabase. The demo must clearly show LoopBite user discovery of affordable nearby low-risk rescue food, checkout reservation, receipt confirmation, merchant listing publishing, and merchant pickup confirmation without complex integrations.

## Goals / Non-Goals

**Goals:**

- Ship the required user routes `/`, `/item/:id`, `/checkout/:itemId`, and `/receipt/:orderId` with a simple, reliable happy path.
- Ship LoopBite Merchant surfaces for My Listings, posting rescue items, seeing reserved orders, and confirming pickup.
- Store merchants, listings, and orders in Supabase Postgres.
- Use Supabase RLS or demo-safe access rules to separate public listing reads, merchant-owned listing writes, and order visibility.
- Keep the UI demo-friendly with clear empty, loading, error, and success states. 

**Non-Goals:**

- No FastAPI or separate backend service.
- No real payment, real delivery integration, Grab/Ahamove integration, admin dashboard, impact dashboard, analytics, recommendation engine, or high-risk food categories.
- No complex merchant onboarding beyond what is needed for the demo.

## Decisions

- Use Supabase client calls directly from the frontend.
  - Rationale: fastest path for a hackathon MVP and matches the brief.
  - Alternative considered: custom API server. Rejected because FastAPI and separate backend work are explicit non-goals.
- Model `listings` as the shared rescue food inventory entity with a `status` field.
  - Rationale: public users need eligible published listings, while merchants need to manage their own listing records.
  - Alternative considered: separate draft and published tables. Rejected as unnecessary for the demo.
- Model `orders` as reservations linked to `listings`.
  - Rationale: users need a receipt and pickup code, while merchants need the same order state to confirm pickup.
  - Alternative considered: receipt-only local state. Rejected because Supabase persistence is required by the brief.
- Keep food categories constrained to `bakery`, `packaged_food`, `dry_noodles`, `cereal`, `snack`, `sealed_drink`, and `other_low_risk`.
  - Rationale: MVP scope is low-risk / quality-based food only.
- Show simple aggregate order counts and active reservations on the merchant listing view.
  - Rationale: satisfies merchant visibility and pickup operations without adding dashboards.
  - Alternative considered: detailed reporting dashboard. Rejected as an explicit non-goal.

## Risks / Trade-offs

- Auth setup may slow the demo -> use the simplest Supabase Auth path needed for merchant ownership and user order ownership.
- Direct frontend writes rely on correct RLS -> keep policies minimal and test each actor path manually.
- Concurrent reservations can oversell listing quantity -> keep the reservation write path focused and verify quantity is still greater than zero before order creation.
- Pickup confirmation touches both `orders` and `listings` -> prefer a single trusted update path when implementation time allows.
- Optional image URLs can break visually -> use a stable fallback item image/card state when no usable URL is present.

## Migration Plan

1. Create Supabase tables and RLS policies.
2. Seed or create merchants and published low-risk listings for the demo.
3. Build the user and merchant routes and connect them to Supabase.
4. Verify the happy path: merchant publishes listing, user reserves listing, receipt renders, merchant confirms pickup.

Rollback is to remove the MVP routes/components and drop the demo Supabase tables or policies if they are no longer needed.

## Open Questions

- Which Supabase Auth method will be used during the demo for user and merchant identities?
- Will demo data be pre-seeded, entered live through the merchant form, or both?
