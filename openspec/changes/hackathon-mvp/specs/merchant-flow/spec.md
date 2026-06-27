## ADDED Requirements

### Requirement: Merchant can view own listings
The system SHALL let target merchants open LoopBite Merchant and view their own rescue food listings.

#### Scenario: Merchant list loads own listings
- **GIVEN** a merchant has created rescue food listings
- **WHEN** the merchant opens My Listings
- **THEN** the system shows only that merchant's listings with item name, food category, status, rescue price, quantity, pickup window, and order count.

#### Scenario: Merchant empty state
- **GIVEN** a merchant has no rescue food listings
- **WHEN** the merchant opens My Listings
- **THEN** the system shows an empty state with a "Post rescue item" action.

### Requirement: Merchant can post a rescue item
The system SHALL allow mini supermarkets, bakeries, convenience stores, and small shops selling low-risk packaged or dry food to post a rescue item.

#### Scenario: Merchant opens post form
- **GIVEN** a merchant is on My Listings
- **WHEN** the merchant clicks "Post rescue item"
- **THEN** the system opens a listing form with fields for `item_name`, `image_url`, `food_category`, `quantity`, `original_price`, `rescue_price`, `pickup_start_time`, `pickup_end_time`, `best_before` / `consume_before`, `quality_note`, `merchant_note`, `fulfillment_options`, and `payment_options`.

#### Scenario: Merchant publishes listing
- **GIVEN** a merchant has entered valid low-risk rescue item information
- **WHEN** the merchant publishes the listing
- **THEN** the system creates a listing owned by that merchant with `status = published` and `risk_group = low_risk_quality_based`.

### Requirement: Merchant listing fields are constrained
The system SHALL store the required LoopBite listing fields for each rescue item.

#### Scenario: Required listing fields are present
- **GIVEN** a merchant publishes a rescue item
- **WHEN** the listing is saved
- **THEN** the listing includes `id`, `merchant_id`, `item_name`, `image_url`, `food_category`, `risk_group`, `quantity`, `original_price`, `rescue_price`, `pickup_start_time`, `pickup_end_time`, `best_before`, `consume_before`, `quality_note`, and `status`.

#### Scenario: Food category uses supported enum
- **GIVEN** a merchant selects a food category
- **WHEN** the listing is validated
- **THEN** `food_category` is one of `bakery`, `packaged_food`, `dry_noodles`, `cereal`, `snack`, `sealed_drink`, or `other_low_risk`.

### Requirement: Merchant listings are low-risk only
The system SHALL prevent MVP merchants from posting high-risk food categories.

#### Scenario: Low-risk listing is accepted
- **GIVEN** a merchant posts bread, dry bakery items, packaged food, cereal, dry noodles, snacks, sealed drinks, or similar low-risk items
- **WHEN** the merchant publishes the listing
- **THEN** the system allows the listing when all required fields are valid.

#### Scenario: High-risk listing is rejected
- **GIVEN** a merchant attempts to post high-risk fresh cooked meals, raw meat, seafood, dairy-heavy items, or unsafe perishables
- **WHEN** the merchant publishes the listing
- **THEN** the system rejects the listing from MVP scope.

### Requirement: Published merchant listing is public only when eligible
The system SHALL make merchant listings visible in the user app only when they satisfy availability and food-scope rules.

#### Scenario: Eligible published listing appears publicly
- **GIVEN** a merchant has published a listing with `quantity > 0`, a valid pickup window, and a low-risk / quality-based category
- **WHEN** a user searches the LoopBite user app
- **THEN** the system includes that listing in the user results.

#### Scenario: Ineligible listing is hidden from user app
- **GIVEN** a listing is not published, has zero quantity, has an expired pickup window, or belongs to a high-risk category
- **WHEN** a user searches the LoopBite user app
- **THEN** the system excludes that listing from orderable user results.

### Requirement: Merchant can see reserved orders
The system SHALL show merchants new orders created when users reserve their listings.

#### Scenario: Merchant sees new reservation
- **GIVEN** a user reserves a merchant listing
- **WHEN** the merchant opens the listing's orders
- **THEN** the system shows the order with `listing_id`, `quantity`, `amount`, `fulfillment_method`, `payment_method`, `payment_status`, `order_status`, and `pickup_code`.

### Requirement: Merchant can confirm pickup
The system SHALL allow a merchant to verify the user's pickup code and confirm pickup.

#### Scenario: Pickup code confirms order
- **GIVEN** an order has `order_status = reserved`
- **WHEN** the merchant checks the user's `pickup_code` and clicks "Confirm pickup"
- **THEN** the system updates `order_status = picked_up`.

#### Scenario: Confirmed pickup decreases quantity
- **GIVEN** a merchant confirms pickup for a reserved order
- **WHEN** the pickup is confirmed
- **THEN** the system decreases the listing quantity by the order quantity.

#### Scenario: Listing becomes sold out
- **GIVEN** a confirmed pickup reduces listing quantity to zero
- **WHEN** the quantity update completes
- **THEN** the system updates listing `status = sold_out`.
