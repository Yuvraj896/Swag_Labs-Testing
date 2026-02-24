import re
import time
import pytest

from playwright.sync_api import Locator, expect, Page
from typing import List

from pages.order_page import OrderPage
from test_data.product_data import  Product, products
from test_data.filter_data import Filter

pytestmark = pytest.mark.order

@pytest.mark.smoke
def test_order_page_visibility(user, order_page_navigate):
    """
    Navigate to order page and assert the visibility of the locators
    """
    page, _  = order_page_navigate
    order_page = OrderPage(page)

    order_page.assert_fields_loaded()


@pytest.mark.parametrize(
    "cart_state",
    [
        "add_some_products",
        "add_all_products"
     ],
     indirect= True
)
@pytest.mark.regression
def test_order_page_product_details(user, order_page_navigate):
    """
    1. Navigate to order page after adding some items to the cart
    2. Assert if the number of products in cart is correct
    3. For each item in cart, assert if the product details matches with the items we added on inventory page
    """
    page, products_in_cart = order_page_navigate
    order_page = OrderPage(page)

    order_page.assert_no_of_items_in_cart(expected_cnt= len(products_in_cart))
    order_page.assert_shopping_badge_value_equal_as_cart_cnt()

    for product in products_in_cart:

        #find the product in inventory
        item_details = order_page.get_item_details(item_name=product.name)
        
        assert item_details["name"] == product.name, f"Name mismatch for {product.name}"
        
        assert item_details["description"] == product.description, f"Description mismatch for {product.name}"

        assert float(item_details["price"].replace("$", "")) == product.price, f"Price mismatch for {product.name}"

@pytest.mark.parametrize(
    "cart_state",
    [
        "add_some_products",
        "add_all_products"
     ],
     indirect= True
)
@pytest.mark.smoke
def test_order_page_grand_total(user, order_page_navigate):
    """
    1. Navigate to the order page after adding some items to the cart
    2. Assert if the number of products in cart is correct
    3. For Every item in Cart, Sum up the prices and checks with the Grand total from UI
    """
    page, added_products = order_page_navigate
    order_page = OrderPage(page)

    order_page.check_grand_total(products_in_cart= added_products)