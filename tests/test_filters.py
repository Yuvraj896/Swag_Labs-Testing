import re
import time
from typing import List
import pytest
from playwright.sync_api import Locator, expect, Page
from pages.dashboard_page import DashboardPage
from test_data.product_data import  Product, products
from test_data.filter_data import Filter

@pytest.mark.parametrize(
        "filter_option",
        list(Filter)[1:],
)
def test_filter_with_no_items(login_as_standard_user, filter_option):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Iterate through each filter option, applies it, and verifies that the products are displayed in the correct order based on the applied filter.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    #apply the filter in ui
    dashboard_page.apply_filter(filter_option)

    # apply filter in sorted list
    sorted_products = Product.sort_products(products, filter_option)

    dashboard_page.assert_product_visible(sorted_products, [])


@pytest.mark.parametrize(
        "filter_option",
        list(Filter)[1:],
)
def test_filter_with_some_items_added_to_cart(add_some_products, filter_option):
    """
    1. Logs in as a standard user, navigates to the inventory page, and adds a few random products to the cart.
    2. Iterates through each filter option, applies it, and verifies that the products are displayed in the correct order based on the applied filter.
    """
    page , added_products = add_some_products
    dashboard_page = DashboardPage(page)

    dashboard_page.apply_filter(filter_option)
    sorted_products = Product.sort_products(products, filter_option)
    dashboard_page.assert_product_visible(products= sorted_products, added_products= added_products)


@pytest.mark.parametrize(
        "filter_option",
        list(Filter)[1:],
)
def test_filter_with_all_items_added_to_cart(add_all_products, filter_option):
    """
    1. Logs in as a standard user, navigates to the inventory page, add all the products to the cart
    2. Iterate through each filter option, applies it
    3. Verfies if the Products are in correct order as expected
    """

    page = add_all_products
    dashboard_page = DashboardPage(page)
    dashboard_page.apply_filter(filter_option)
    sorted_products = Product.sort_products(products, filter_option)
    dashboard_page.assert_product_visible(products= sorted_products, added_products= products)