# LoopBite MVP Use Cases

## 1. Actors

- **User**: A student, low-income user, late-night eater, or nearby food seeker looking for affordable rescue food.
- **Merchant**: A mini supermarket, bakery, convenience store, or small shop selling low-risk packaged or dry food.

## 2. Target Merchants

- mini supermarkets
- bakeries
- convenience stores
- small shops selling low-risk packaged or dry food

## 3. Food Scope

LoopBite MVP supports only low-risk, quality-based food items:

- bread
- dry bakery items
- packaged food
- cereal
- dry noodles
- snacks
- sealed drinks
- similar low-risk shelf-stable or quality-based items

The MVP excludes high-risk fresh cooked meals, raw meat, seafood, dairy-heavy items, and unsafe perishables.

## 4. Routes

- `/`: Search, geolocation request, and nearby rescue food Map + List view.
- `/item/:id`: Rescue food item detail page.
- `/checkout/:itemId`: Checkout for fulfillment and payment method selection.
- `/receipt/:orderId`: Receipt with pickup code and order status.

## 5. User Discovery Flow

1. User opens LoopBite at `/`.
2. User searches for food by keyword.
3. App requests geolocation.
4. App shows nearby rescue food in a combined Map + List view.
5. User filters rescue food by:
   - `food_category`
   - distance
   - price
   - pickup window
   - `best_before` / `consume_before`
   - availability
6. User opens `/item/:id`.
7. User sees item details:
   - item name
   - image
   - merchant name
   - `food_category`
   - risk group: low-risk / quality-based
   - original price
   - rescue price
   - quantity left
   - pickup window
   - `best_before` / `consume_before`
   - short quality note

## 6. User Checkout and Receipt Flow

1. User opens `/checkout/:itemId` from an eligible rescue food item.
2. User chooses `fulfillment_method`:
   - `pickup`
   - `delivery_mock` only if time allows
3. User chooses `payment_method`:
   - `pay_at_counter`
   - `pay_online_mock`
4. User confirms the order.
5. System creates an order, generates a `pickup_code`, and reserves quantity.
6. App redirects to `/receipt/:orderId`.
7. User sees a receipt with pickup code, pickup time, merchant address, amount, and order status.

## 7. Merchant Listing Flow

1. Merchant opens LoopBite Merchant.
2. Merchant opens My Listings.
3. Merchant clicks "Post rescue item".
4. Merchant enters:
   - `item_name`
   - `image_url`
   - `food_category`
   - `quantity`
   - `original_price`
   - `rescue_price`
   - `pickup_start_time`
   - `pickup_end_time`
   - `best_before` / `consume_before`
   - `quality_note`
   - `merchant_note`
   - `fulfillment_options`
   - `payment_options`
5. Merchant publishes the item.
6. Item appears in the user app only if:
   - `status = published`
   - `quantity > 0`
   - pickup window is still valid
   - item belongs to a low-risk / quality-based category
7. When a user reserves the item, merchant sees the new order.
8. Merchant checks the `pickup_code` from the user.
9. Merchant clicks "Confirm pickup".
10. System updates:
    - `order_status = picked_up`
    - quantity decreases
    - if `quantity = 0`, listing status becomes `sold_out`

## 8. Listing Fields

- `id`
- `merchant_id`
- `item_name`
- `image_url`
- `food_category`
- `risk_group` default `"low_risk_quality_based"`
- `quantity`
- `original_price`
- `rescue_price`
- `pickup_start_time`
- `pickup_end_time`
- `best_before`
- `consume_before`
- `quality_note`
- `status`

## 9. Food Category Enum

- `bakery`
- `packaged_food`
- `dry_noodles`
- `cereal`
- `snack`
- `sealed_drink`
- `other_low_risk`

## 10. Order Fields

- `id`
- `listing_id`
- `quantity`
- `amount`
- `fulfillment_method`
- `payment_method`
- `payment_status`
- `order_status`
- `pickup_code`

## 11. Order Statuses

- `reserved`
- `picked_up`
- `cancelled`
- `expired`

## 12. Edge Cases

- **Missing item**: Show a not-found state and allow navigation back to `/`.
- **Unavailable item**: Prevent checkout when availability is false, quantity is zero, or the pickup window has passed.
- **High-risk category**: Exclude unsupported food categories from MVP listings and checkout.
- **Location denied**: Keep keyword search available and show a clear state explaining that nearby sorting requires location.
- **Failed order creation**: Show an error state, do not redirect to receipt, and allow retry.
- **Expired reservation**: Show the order as `expired` and do not allow pickup confirmation.
- **Invalid pickup code**: Merchant cannot confirm pickup until the provided code matches the reserved order.
- **Sold-out listing**: When confirmed pickups reduce quantity to zero, the listing is marked `sold_out` and no longer appears as orderable.

## 13. Explicit Non-Goals

- No real payment.
- No real delivery integration.
- No Grab/Ahamove integration.
- No admin dashboard.
- No impact dashboard.
- No FastAPI backend.
- No high-risk food categories.
- No raw meat, seafood, dairy-heavy items, unsafe perishables, or fresh cooked meal handling in MVP scope.
