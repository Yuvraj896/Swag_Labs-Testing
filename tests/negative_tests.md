# 🔻 Negative Test Coverage

| Test ID | Test Function                                                                | Precondition / Setup         | Test Steps                                  | Expected Result                        | Module / Area |
| ------- | ---------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------- | -------------------------------------- | ------------- |
| NEG-001 | test_checkout_validation_errors[chromium--Doe-12345-login_as_standard_user]  | Standard user, checkout page | Enter invalid checkout data                 | Proper error validation                | Checkout      |
| NEG-002 | test_problem_user_filter[chromium-Name (Z to A)]                             | Logged in as problem user    | Apply filter Name (Z → A)                   | UI shows broken behavior               | Filters       |
| NEG-003 | test_error_user_filter[chromium-Name (Z to A)]                               | Logged in as error user      | Apply filter Name (Z → A)                   | Dialog appears, filter applied         | Filters       |
| NEG-004 | test_login_not_work[chromium]                                                | Locked out user              | Attempt login                               | Login fails                            | Login         |
| NEG-005 | test_product_images_in_problem_user[chromium]                                | Logged in as problem user    | Navigate to inventory, check product images | Broken images visible                  | Inventory     |
| NEG-006 | test_other_user_add_and_remove_from_cart[chromium-login_as_problem_user]     | Problem user, inventory page | Add/remove products in cart                 | Only allowed items added, remove fails | Inventory     |
| NEG-007 | test_remove_button_not_working[chromium-login_as_problem_user]               | Problem user, inventory page | Attempt to remove products                  | Remove doesn’t work for some products  | Inventory     |
| NEG-008 | test_checkout_validation_errors[chromium-John--12345-login_as_standard_user] | Standard user, checkout page | Enter invalid checkout data                 | Proper error validation                | Checkout      |
| NEG-009 | test_problem_user_filter[chromium-Price (low to high)]                       | Logged in as problem user    | Apply Price (low → high)                    | Problem behavior visible               | Filters       |
| NEG-010 | test_error_user_filter[chromium-Price (low to high)]                         | Logged in as error user      | Apply Price (low → high)                    | Dialog appears, filter applied         | Filters       |
| NEG-011 | test_other_user_add_and_remove_from_cart[chromium-login_as_error_user]       | Error user, inventory page   | Add/remove products in cart                 | Only allowed items added, remove fails | Inventory     |
| NEG-012 | test_remove_button_not_working[chromium-login_as_error_user]                 | Error user, inventory page   | Attempt to remove products                  | Remove doesn’t work for some products  | Inventory     |
| NEG-013 | test_checkout_validation_errors[chromium-John-Doe--login_as_standard_user]   | Standard user, checkout page | Enter invalid checkout data                 | Proper error validation                | Checkout      |
| NEG-014 | test_problem_user_filter[chromium-Price (high to low)]                       | Logged in as problem user    | Apply Price (high → low)                    | Problem behavior visible               | Filters       |
| NEG-015 | test_error_user_filter[chromium-Price (high to low)]                         | Logged in as error user      | Apply Price (high → low)                    | Dialog appears, filter applied         | Filters       |

---