# Skill: elderly_meal_express (長者餐點快捷訂單)

## Description
自動化執行 Uber Eats 訂餐流程，專為 90 歲長者設計的軟食組合，將搜尋、配餐、備註自動化，最後交由用戶完成支付。

## Parameters
- `restaurant_type` (string, default: "粥品"): 搜尋的餐廳類型。
- `main_dish` (string, default: "魚片粥"): 主餐品項。
- `side_dish` (string, default: "蒸蛋"): 配餐品項。
- `delivery_address` (string, default: "台中市惠中路一段 198 號"): 配送地址。
- `special_note` (string, default: "給 90 歲長者食用，請將肉類切碎、蔬菜煮爛，謝謝！"): 訂單備註。

## Execution Workflow
1. **Browser Setup**: 
   - Open `https://www.ubereats.com/`.
   - Check if user is logged in. If not, pause and prompt user to log in.
2. **Address Setup**: 
   - Navigate to address setting and input `delivery_address`.
3. **Restaurant Selection**: 
   - Search for `restaurant_type`.
   - Filter by "High Rating" and "Short Delivery Time".
   - Enter the top recommended shop (Prefer "粥爺 惠中店").
4. **Carting**: 
   - Find and add `main_dish` to cart.
   - Find and add `side_dish` to cart.
5. **Note Entry**: 
   - Navigate to Checkout/Cart page.
   - Locate "Special Instructions" field and input `special_note`.
6. **Handover**: 
   - Provide the final checkout URL to the user for payment.

## Error Handling
- If `main_dish` is unavailable, substitute with "瘦肉粥" and notify user.
- If the restaurant is closed, move to the next highly-rated alternative.
