import re
import pytest
from playwright.sync_api import Locator, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from test_data.product_data import products
from test_data.filter_data import Filter
from tests.conftest import login
from pages.cart_page import CartPage

pytestmark = pytest.mark.cookies

@pytest.mark.parametrize(
    "cart_state",
    [
        "add_some_products",
        "add_all_products"
    ],
    indirect= True
)
@pytest.mark.regression
def test_cart_state_with_cookies(cart_state):
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
    

@pytest.mark.parametrize(
    "user", ["login_as_standard_user"], indirect=True
)
@pytest.mark.parametrize(
    "cart_state", 
    [
        "add_some_products",
        "add_all_products"
     ],
     indirect= True
)
@pytest.mark.regression
def test_cart_page_state_cookie_session(cart_page_with_products, user):
    """
    1. Login for each user, add the items to the cart and navigate to cart page
    2. Assert Expected count in the cart
    3. Log out from the page
    4. Login again and navigate to the cart page
    5. Check if the items added in the cart matches with the one we added before
    """
    
    page, added_products = cart_page_with_products
    cart_page = CartPage(page)
    
    cart_page.relogin_and_navigate_to_cart_page(username="standard_user")
    cart_page.check_products_data(products_in_cart=added_products)