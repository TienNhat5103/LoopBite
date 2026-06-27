## ADDED Requirements

### Requirement: User can search nearby rescue food
The system SHALL let users search LoopBite rescue food by keyword from `/` and request geolocation before showing nearby results.

#### Scenario: Keyword search requests location
- **GIVEN** a user opens LoopBite at `/`
- **WHEN** the user searches for food by keyword
- **THEN** the system requests geolocation and uses the response to find nearby rescue food.

#### Scenario: Location denial is handled
- **GIVEN** a user searches for food by keyword
- **WHEN** the user denies geolocation
- **THEN** the system keeps search available and shows a clear state explaining that nearby sorting requires location.

### Requirement: User can view rescue food in Map and List views
The system SHALL show nearby eligible rescue food in a combined Map + List view after search and location handling.

#### Scenario: Nearby rescue food results render
- **GIVEN** one or more available eligible rescue food items exist near the user
- **WHEN** search and location handling complete
- **THEN** the system shows those items in Map + List view with item name, merchant name, rescue price, distance, pickup window, and availability.

#### Scenario: Unavailable rescue food is not shown as orderable
- **GIVEN** rescue food items exist with zero quantity, unavailable status, or expired pickup windows
- **WHEN** the user views search results
- **THEN** the system does not present those items as orderable.

### Requirement: Rescue food scope is low-risk and quality-based
The system SHALL limit MVP rescue food to low-risk, quality-based items.

#### Scenario: Supported food categories are eligible
- **GIVEN** food items are categorized as bread, dry bakery items, packaged food, cereal, dry noodles, snacks, sealed drinks, or similar low-risk items
- **WHEN** the user searches LoopBite
- **THEN** the system may include those items in results when they are available.

#### Scenario: High-risk food categories are excluded
- **GIVEN** food items are raw meat, seafood, dairy-heavy items, unsafe perishables, or high-risk fresh cooked meals
- **WHEN** the user searches LoopBite
- **THEN** the system excludes those items from MVP results and checkout.

### Requirement: User can filter rescue food results
The system SHALL allow users to filter nearby rescue food by food category, distance, price, pickup window, best-before or consume-before timing, and availability.

#### Scenario: User applies filters
- **GIVEN** nearby rescue food results are shown
- **WHEN** the user filters by `food_category`, distance, price, pickup window, `best_before` / `consume_before`, or availability
- **THEN** the system updates the Map + List view to show only matching rescue food.

### Requirement: User can open rescue food details
The system SHALL allow a user to open a rescue food item detail page at `/item/:id`.

#### Scenario: Item detail loads
- **GIVEN** an available low-risk rescue food item exists
- **WHEN** a user opens `/item/:id`
- **THEN** the system shows item name, image, merchant name, `food_category`, risk group, original price, rescue price, quantity left, pickup window, `best_before` / `consume_before`, and a short quality note.

#### Scenario: Item detail identifies risk group
- **GIVEN** a rescue food item is displayed on `/item/:id`
- **WHEN** the item detail page renders
- **THEN** the system shows the risk group as low-risk / quality-based.

#### Scenario: Missing item is handled
- **GIVEN** no eligible rescue food item exists for the requested id
- **WHEN** a user opens `/item/:id`
- **THEN** the system shows a clear not-found or unavailable state.

### Requirement: User can proceed to checkout
The system SHALL provide a checkout action from eligible item details that opens `/checkout/:itemId`.

#### Scenario: Checkout action is available for eligible item
- **GIVEN** a user is viewing an available low-risk rescue food item detail page
- **WHEN** the item detail page renders
- **THEN** the system shows a checkout action that starts the order flow at `/checkout/:itemId`.
