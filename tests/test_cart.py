import re
import pytest
import time
from playwright.sync_api import Locator, expect
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

pytestmark = pytest.mark.cart

@pytest.mark.parametrize("user", ["login_as_standard_user"], indirect=True)
@pytest.mark.smoke
def test_cart_elements_visibility(cart_page_navigate):
    """
    1. Login as whatever user and navigate to the Cart page
    2. Assert the visibility of the Locators
    """
    
    page = cart_page_navigate
    cart_page = CartPage(page)

    cart_page.check_page_locators_visibility()


@pytest.mark.parametrize(
    "user", ["login_as_standard_user"], indirect=True
)
@pytest.mark.parametrize(
    "cart_state", 
    [
        "add_no_products",
        "add_some_products",
        "add_all_products"
     ],
     indirect= True
)
@pytest.mark.regression
def test_cart_products_visibility(cart_page_with_products, user) :
    """
    1. Login for each user and add Required items to the cart and navigate to the cart page
    2. Now check if the added products details matches with the ones that we added on the dashboard page
    """
    
    page, added_products = cart_page_with_products
    cart_page = CartPage(page)

    cart_page.check_products_data(products_in_cart=added_products)


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
def test_remove_button_work(cart_page_with_products, user):
    """
    1. Login as some user and navigate to the cart page
    2. Remove item sequentially and check if the badge value decrements
    """

    page, added_products = cart_page_with_products
    cart_page = CartPage(page)

    no_of_items_added = len(added_products)
    cart_page.assert_product_count_in_cart(expected_count=no_of_items_added)

    current_items = no_of_items_added
    for product in added_products:
        cart_page.press_remove_button(item_name=product.name)
        current_items -= 1
        cart_page.assert_product_count_in_cart(expected_count=current_items)
        cart_page.assert_shopping_badge_value_equal_as_cart_cnt()



