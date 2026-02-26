
# Architecture

## 🔹 Design Pattern

This framework follows a **Page Object Model (POM)** architecture with:

* Page layer (UI interaction)
* Test layer (validation & orchestration)
* Data layer (Products, Filters, allowed cart behavior)
* Fixture layer (environment + state control)

---

## 📂 Project Structure

```
project/
│
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── order_page.py
│
├── test_data/
│   ├── product_data.py
│   └── filter_data.py
│
├── tests/
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   ├── test_filters.py
│   ├── test_cookie.py
│   ├── test_order.py
│   └── test_login.py
│
├── conftest.py
├── pytest.ini
└── README.md
```
# 👥 User Types Covered

| User            | Behavior Tested                   |
| --------------- | --------------------------------- |
| standard_user   | Normal full flow                  |
| problem_user    | Broken images + inconsistent cart |
| error_user      | Dialog popups during filtering    |
| locked_out_user | Login failure validation          |
| visual_user     | UI validation cases               |


---

# 🧱 Framework Layers

## 1️⃣ Page Layer (POM)

Each page encapsulates:

* Selectors
* Locators
* Navigation
* UI actions
* UI-level assertions

Pages implemented:

* `LoginPage`
* `DashboardPage`
* `CartPage`
* `CheckoutPage`
* `OrderPage`

---

## 2️⃣ Data Layer

### 🔹 Product Model

`Product` dataclass:

* id
* name
* price
* description
* image_path

Includes:

* `sort_products()` → used to validate UI filter sorting

---

### 🔹 Filter Enum

`Filter` (StrEnum)

Supports:

* Name A → Z
* Name Z → A
* Price low → high
* Price high → low

Used for parameterized sorting tests.

---

### 🔹 Cart Behavior Matrix

`allowed_cart` dictionary defines:

* Which products can be added/removed for specific negative users

Used for:

* Problem user tests
* Error user tests

---

# 🔁 Fixture Architecture

The framework uses layered fixtures for clean state management.

## 🔹 Dependency Tree

```
playwright (session)
└── browser (function)
    └── context (function)
        └── page (function)
            └── login
                └── login_as_* 
                    └── user
                        ├── add_*_products
                        │    └── cart_state
                        │         └── cart_page_with_products
                        │              └── order_page_navigate
                        │
                        └── cart_page_navigate
                             └── checkout_page_navigate
```

---

## 🔹 Key Fixtures

| Fixture                  | Purpose                         |
| ------------------------ | ------------------------------- |
| `browser`                | Launch Playwright browser       |
| `context`                | Isolated browser context        |
| `page`                   | Page instance                   |
| `login`                  | Generic login helper            |
| `user`                   | Dynamically resolves login type |
| `cart_state`             | Resolves cart content state     |
| `add_no_products`        | Empty cart                      |
| `add_some_products`      | Random 3 products               |
| `add_all_products`       | All products                    |
| `checkout_page_navigate` | Navigates to checkout page      |
| `order_page_navigate`    | Navigates to order page         |

---

# 🧪 Test Strategy

The suite is organized by functional areas using markers.

---

# 🗂 Test Coverage Table

| Area              | Test File           | Coverage                                         |
| ----------------- | ------------------- | ------------------------------------------------ |
| Login             | `test_invalid_login.py`     | Locked user validation                           |
| Inventory         | `test_inventory.py` | UI visibility, product details, add/remove logic |
| Cart              | `test_cart.py`      | Cart state, remove logic, badge validation       |
| Checkout          | `test_checkout.py`  | Successful checkout + validation errors          |
| Order             | `test_order.py`     | Order summary, price validation, grand total     |
| Filters           | `test_filters.py`   | Sorting behavior (positive + negative users)     |
| Cookies / Session | `test_cookie.py`    | Cart persistence after logout/login              |
| Snapshot          | `test_inventory.py` | Product image validation                         |

---
# 🧪 Test Coverage

For full test coverage, see:

- [Smoke Tests](tests/smoke_tests.md)
- [Regression Tests](tests/regression_tests.md)
- [Negative Tests](tests/negative_tests.md)





# ▶ Running Tests

## Install Dependencies

for any running related help
```bash
make help
```

---

## Run All Tests

```bash
pytest
```

---

## Run By Marker

```bash
make <MARKER_NAME> ARGS="<OTHER ARGUMENTS>"
```

---
## Run Generalized
```bash
make run MARKERS="<MARKER_NAMES>" ARGS="<OTHER ARGUMENTS>"
```
---

