import re
import pytest
from playwright.sync_api import Locator, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from test_data.product_data import products
from test_data.filter_data import Filter
from tests.conftest import login


@pytest.mark.parametrize(
    "cart_state",
    [
        "add_no_products",
        "add_some_products",
        "add_all_products"
    ],
    indirect= True
)
def test_cart_state_with_cookies(cart_state, request):
    """
    1. Logins and add products (no, some, all) in the cart
    2. Logs out
    3. Logins again
    4. Verify if the cart state changed
    """
    # Lets assume the fixture adds the products to cart as expected

    page, added_products = cart_state
    dashboard_page = DashboardPage(page)
    dashboard_page.logout()

    # login again
    login_page = LoginPage(page)
    login_page.login("standard_user", "secret_sauce")

    dashboard_page.is_inventory_page()

    # verify the cart state
    dashboard_page.assert_product_visible(products= products, added_products= added_products)
    
