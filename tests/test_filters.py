import re
from typing import List
import pytest
from playwright.sync_api import Locator, expect
from pages.dashboard_page import DashboardPage
from utils import FilterValue, Product, products


def test_filter_with_no_items(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Iterate through each filter option, applies it, and verifies that the products are displayed in the correct order based on the applied filter.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()

    filters = list(FilterValue)

    for filter in filters[1:] :
        print(f"Applying filter: {filter.filter_name}")
        dashboard_page.apply_filter(filter.filter_value)

        sorted_products = Product.sort_products(products, filter)
        dashboard_page.assert_product_visible(sorted_products, [])

def test_filter_with_items_in_cart(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Adds a few products to the cart.
    3. Iterate through each filter option, applies it, and verifies that the products are displayed in the correct order based on the applied filter, ensuring that the cart functionality does not interfere with the sorting.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()

    # Add first two products to cart
    dashboard_page.click_add_to_cart(index=2)
    dashboard_page.click_add_to_cart(index=3)

    added_products = [2,3]

    filters = list(FilterValue)

    for filter in filters[1:] :
        print(f"Applying filter: {filter.filter_name}")
        dashboard_page.apply_filter(filter.filter_value)

        sorted_products = Product.sort_products(products, filter)
        dashboard_page.assert_product_visible(sorted_products, added_products)