## ADDED Requirements

### Requirement: User can choose fulfillment method
The system SHALL allow a user to choose a fulfillment method during checkout at `/checkout/:itemId`.

#### Scenario: Pickup fulfillment is available
- **GIVEN** a user is checking out an available rescue food item
- **WHEN** the checkout page renders
- **THEN** the system allows the user to choose `pickup` as the fulfillment method.

#### Scenario: Mock delivery remains optional and non-integrated
- **GIVEN** the MVP includes delivery selection only if time allows
- **WHEN** the checkout page renders a delivery option
- **THEN** the system labels it as `delivery_mock` and does not call Grab, Ahamove, or any real delivery integration.

### Requirement: User can choose payment method
The system SHALL allow a user to choose a mock or offline payment method during checkout.

#### Scenario: Pay at counter is available
- **GIVEN** a user is checking out an available rescue food item
- **WHEN** the user selects payment
- **THEN** the system allows `pay_at_counter`.

#### Scenario: Online payment is mock only
- **GIVEN** a user is checking out an available rescue food item
- **WHEN** the user selects `pay_online_mock`
- **THEN** the system does not collect real payment details and does not call a payment provider.

### Requirement: User can confirm a rescue food order
The system SHALL allow a user to confirm an order for an available low-risk rescue food item.

#### Scenario: Order confirmation creates reservation
- **GIVEN** a user is checking out an available rescue food item with quantity left
- **WHEN** the user confirms the order
- **THEN** the system creates an order, generates a `pickup_code`, reserves quantity, and sets order status to `reserved`.

#### Scenario: Unavailable item cannot be reserved
- **GIVEN** a rescue food item has zero quantity, unavailable status, unsupported high-risk category, or an expired pickup window
- **WHEN** the user attempts to confirm checkout
- **THEN** the system prevents order creation and shows an unavailable state.

### Requirement: User is redirected to receipt
The system SHALL redirect the user to `/receipt/:orderId` after a rescue food order is created.

#### Scenario: Successful order redirects to receipt
- **GIVEN** an order was created successfully with a `pickup_code`
- **WHEN** the checkout flow finishes
- **THEN** the system redirects the user to `/receipt/:orderId`.

### Requirement: Receipt shows pickup and order details
The system SHALL show a receipt for the rescue food order.

#### Scenario: Receipt renders pickup details
- **GIVEN** an order exists with linked item and merchant details
- **WHEN** a user opens `/receipt/:orderId`
- **THEN** the system shows pickup code, pickup time, merchant address, amount, and order status.

#### Scenario: Missing receipt is handled
- **GIVEN** no order exists for the requested order id
- **WHEN** a user opens `/receipt/:orderId`
- **THEN** the system shows a clear not-found or unavailable receipt state.

### Requirement: Order fields are constrained
The system SHALL store the required LoopBite order fields for each reservation.

#### Scenario: Required order fields are present
- **GIVEN** a user reserves a rescue food listing
- **WHEN** the order is saved
- **THEN** the order includes `id`, `listing_id`, `quantity`, `amount`, `fulfillment_method`, `payment_method`, `payment_status`, `order_status`, and `pickup_code`.

### Requirement: Order statuses are constrained
The system SHALL use only the supported LoopBite order statuses for the MVP.

#### Scenario: Supported statuses are used
- **GIVEN** an order exists
- **WHEN** the system displays or updates the order status
- **THEN** the status is one of `reserved`, `picked_up`, `cancelled`, or `expired`.

### Requirement: Merchant can complete pickup orders
The system SHALL allow a merchant to confirm pickup for a reserved order using the user's pickup code.

#### Scenario: Merchant confirms pickup code
- **GIVEN** an order has `order_status = reserved`
- **WHEN** the merchant checks the user's `pickup_code` and confirms pickup
- **THEN** the system updates `order_status = picked_up`.

#### Scenario: Pickup confirmation updates listing availability
- **GIVEN** a merchant confirms pickup for a reserved order
- **WHEN** the order status becomes `picked_up`
- **THEN** the system decreases listing quantity by the order quantity and sets listing status to `sold_out` if quantity reaches zero.

### Requirement: MVP excludes real payment and delivery integrations
The system SHALL keep checkout integrations mock-only for the MVP.

#### Scenario: Checkout has no real external integrations
- **GIVEN** a user completes checkout
- **WHEN** the order is confirmed
- **THEN** the system does not call real payment providers, Grab, Ahamove, or any real delivery service.
