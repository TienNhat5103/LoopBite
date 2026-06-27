## ADDED Requirements

### Requirement: User can browse published campaigns
The system SHALL show published campaign cards on the landing page at `/`.

#### Scenario: Landing page shows published campaigns
- **GIVEN** one or more published campaigns exist in Supabase
- **WHEN** a user opens `/`
- **THEN** the system shows campaign cards with the campaign title, merchant name, discounted price, and impact summary.

#### Scenario: Landing page excludes unpublished campaigns
- **GIVEN** published and unpublished campaigns exist in Supabase
- **WHEN** a user opens `/`
- **THEN** the system shows only published campaigns.

### Requirement: User can open campaign details
The system SHALL allow a user to open a campaign detail page at `/campaign/:id`.

#### Scenario: Campaign detail loads
- **GIVEN** a published campaign exists
- **WHEN** a user selects that campaign from the landing page
- **THEN** the system opens `/campaign/:id` and shows title, merchant name, description, original price, discounted price, quantity, image if available, and impact message.

#### Scenario: Missing campaign is handled
- **GIVEN** no published campaign exists for the requested id
- **WHEN** a user opens `/campaign/:id`
- **THEN** the system shows a clear not-found or unavailable state.

### Requirement: User can start support action
The system SHALL provide a clear support, buy, or reserve action from the campaign detail page.

#### Scenario: Support action is available
- **GIVEN** a user is viewing a published campaign detail page
- **WHEN** the campaign detail page renders
- **THEN** the system shows a "Support", "Buy", or "Reserve" action that starts the mock order confirmation.
