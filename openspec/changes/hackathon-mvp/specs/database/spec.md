## ADDED Requirements

### Requirement: Database supports both LoopBite apps
The system SHALL use one Supabase Postgres database contract for the LoopBite user app and LoopBite Merchant app.

#### Scenario: Core tables are present
- **GIVEN** the MVP database is initialized
- **WHEN** the apps access Supabase
- **THEN** the database exposes `merchants`, `listings`, and `orders` as the core MVP tables.

#### Scenario: Optional profiles are isolated
- **GIVEN** Supabase Auth is not required for the demo path
- **WHEN** the database is initialized
- **THEN** `profiles` is optional and is not required for user discovery, listing publication, order creation, receipt display, or pickup confirmation.

### Requirement: Database constrains low-risk listing data
The system SHALL enforce the LoopBite low-risk / quality-based listing model.

#### Scenario: Listing category enum is constrained
- **GIVEN** a merchant creates or updates a listing
- **WHEN** `food_category` is saved
- **THEN** it is one of `bakery`, `packaged_food`, `dry_noodles`, `cereal`, `snack`, `sealed_drink`, or `other_low_risk`.

#### Scenario: Risk group defaults to low-risk
- **GIVEN** a merchant creates a listing
- **WHEN** the listing is saved
- **THEN** `risk_group` defaults to `low_risk_quality_based`.

#### Scenario: Listing values are valid
- **GIVEN** a merchant creates or updates a listing
- **WHEN** the listing is validated
- **THEN** quantity is non-negative, prices are non-negative, `rescue_price` is not greater than `original_price`, and `pickup_end_time` is later than `pickup_start_time`.

### Requirement: User app reads eligible public listings
The system SHALL expose only eligible listings to the LoopBite user app discovery and detail flows.

#### Scenario: Eligible listing is readable by user app
- **GIVEN** a listing has `status = published`, `quantity > 0`, a valid future pickup window, and `risk_group = low_risk_quality_based`
- **WHEN** the user app searches or opens item detail
- **THEN** the listing can be read with merchant name, merchant address, optional location, item details, prices, pickup window, quality note, fulfillment options, and payment options.

#### Scenario: Ineligible listing is hidden from user app
- **GIVEN** a listing is draft, sold out, expired, cancelled, zero quantity, outside the pickup window, or outside the low-risk food scope
- **WHEN** the user app searches or opens item detail
- **THEN** the listing is not presented as orderable.

### Requirement: User app creates reservations
The system SHALL allow the user app to create order reservations for eligible listings.

#### Scenario: Reservation creates order
- **GIVEN** a user checks out an eligible listing
- **WHEN** the order is saved
- **THEN** the database stores `listing_id`, `quantity`, `amount`, `fulfillment_method`, `payment_method`, `payment_status`, `order_status = reserved`, and a generated `pickup_code`.

#### Scenario: Receipt can be loaded
- **GIVEN** an order exists
- **WHEN** the user app opens `/receipt/:orderId`
- **THEN** the database can return the order joined with listing and merchant details needed for pickup code, pickup time, merchant address, amount, and order status.

### Requirement: Merchant app manages own listings
The system SHALL allow the merchant app to create, publish, and manage only the merchant's own listings.

#### Scenario: Merchant listing write is scoped
- **GIVEN** a merchant creates or edits a listing
- **WHEN** the database saves the row
- **THEN** the row is associated with that merchant's `merchant_id`.

#### Scenario: My Listings can be loaded
- **GIVEN** a merchant has listings
- **WHEN** the merchant app opens My Listings
- **THEN** the database can return only that merchant's listings with item name, food category, status, rescue price, quantity, pickup window, and order counts.

### Requirement: Merchant app completes pickup
The system SHALL support merchant pickup confirmation from the shared order and listing data.

#### Scenario: Merchant reads reserved orders
- **GIVEN** users have reserved a merchant's listings
- **WHEN** the merchant app opens listing orders
- **THEN** the database can return orders for that merchant's listings with quantity, amount, fulfillment method, payment method, payment status, order status, and pickup code.

#### Scenario: Pickup confirmation updates order and listing
- **GIVEN** a reserved order has a matching `pickup_code`
- **WHEN** the merchant confirms pickup
- **THEN** the database supports setting `order_status = picked_up`, decreasing listing quantity by the order quantity, and setting listing `status = sold_out` when quantity reaches zero.

### Requirement: Database excludes non-goal integration data
The system SHALL not require database structures for non-goal integrations in the MVP.

#### Scenario: Non-goal tables are absent
- **GIVEN** the MVP database is initialized
- **WHEN** implementation follows the finalized database contract
- **THEN** the database does not require tables for real payments, real delivery integration, Grab/Ahamove integration, admin dashboards, impact dashboards, FastAPI services, or high-risk food category handling.
