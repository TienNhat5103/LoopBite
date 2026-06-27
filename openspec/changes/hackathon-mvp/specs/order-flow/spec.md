## ADDED Requirements

### Requirement: User can confirm a mock order
The system SHALL allow a user to confirm a mock support, buy, or reserve order for a published campaign.

#### Scenario: Mock order confirmation creates records
- **GIVEN** a user is confirming support for a published campaign
- **WHEN** the user confirms the mock order
- **THEN** the system creates an order in Supabase for the campaign and creates an impact event linked to that order.

#### Scenario: Mock order has no real payment
- **GIVEN** a user is confirming support for a campaign
- **WHEN** the user completes the mock order flow
- **THEN** the system does not collect payment details or call a payment provider.

### Requirement: User is redirected to receipt
The system SHALL redirect the user to `/receipt/:orderId` after a mock order is created.

#### Scenario: Successful order redirects to receipt
- **GIVEN** an order and impact event were created successfully
- **WHEN** the mock order flow finishes
- **THEN** the system redirects the user to `/receipt/:orderId`.

### Requirement: Receipt shows contribution details
The system SHALL show a simple confirmation and impact receipt for the order.

#### Scenario: Receipt renders order and impact details
- **GIVEN** an order exists with a linked campaign, merchant, and impact event
- **WHEN** a user opens `/receipt/:orderId`
- **THEN** the system shows the campaign name, merchant name, order amount, donation or impact message, and thank-you message.

#### Scenario: Missing receipt is handled
- **GIVEN** no order exists for the requested order id
- **WHEN** a user opens `/receipt/:orderId`
- **THEN** the system shows a clear not-found or unavailable receipt state.

### Requirement: Supabase access rules protect orders
The system SHALL enforce the minimum RLS behavior required for mock orders.

#### Scenario: User creates own order
- **GIVEN** an authenticated user is supporting a published campaign
- **WHEN** the user confirms the mock order
- **THEN** Supabase allows the user to create their own order.

#### Scenario: Merchant reads related orders
- **GIVEN** orders exist for a merchant's campaigns
- **WHEN** the merchant views their campaign list
- **THEN** Supabase allows the merchant to read orders related to their own campaigns.
