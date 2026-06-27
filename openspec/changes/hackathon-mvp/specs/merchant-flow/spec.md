## ADDED Requirements

### Requirement: Merchant can view own campaigns
The system SHALL show a merchant's own campaign list at `/merchant`.

#### Scenario: Merchant list loads own campaigns
- **GIVEN** a merchant has created campaigns
- **WHEN** the merchant opens `/merchant`
- **THEN** the system shows only that merchant's campaigns with title, status, discounted price, quantity, and simple order count.

#### Scenario: Merchant empty state
- **GIVEN** a merchant has no campaigns
- **WHEN** the merchant opens `/merchant`
- **THEN** the system shows an empty state with a create campaign action.

### Requirement: Merchant can create a campaign
The system SHALL allow a merchant to create a campaign at `/merchant/campaigns/new`.

#### Scenario: Merchant opens create form
- **GIVEN** a merchant is on `/merchant`
- **WHEN** the merchant clicks "Create campaign"
- **THEN** the system opens `/merchant/campaigns/new` with fields for title, description, original price, discounted price, quantity, donation rate or impact message, and optional image URL.

#### Scenario: Merchant publishes campaign
- **GIVEN** a merchant has entered valid campaign information
- **WHEN** the merchant publishes the campaign
- **THEN** the system creates a published campaign in Supabase owned by that merchant.

### Requirement: Published merchant campaign is public
The system SHALL make published merchant campaigns visible to users on the landing page.

#### Scenario: Published campaign appears publicly
- **GIVEN** a merchant has published a campaign
- **WHEN** a user opens `/`
- **THEN** the system includes that campaign in the public campaign cards.

### Requirement: Merchant can see campaign order count
The system SHALL show a simple order count per merchant campaign.

#### Scenario: Order count updates from orders
- **GIVEN** users have created mock orders for a merchant campaign
- **WHEN** the merchant opens `/merchant`
- **THEN** the system shows the number of orders for that campaign.
