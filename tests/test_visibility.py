import re
import pytest
from playwright.sync_api import Locator, expect
from pages.dashboard_page import DashboardPage
from utils import products


def test_dashboard_elements_visibility(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Asserts the visibility of the primary header, page heading, burger menu button, shopping cart button, filter button, and products title.
    3. Asserts the visibility of each product on the inventory page.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.assert_page_headers_visible()
    dashboard_page.assert_product_visible(products, [])


def test_each_product_page(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Iterates through each product on the inventory page, clicks on it, and verifies that the product details page displays the correct name, description, price, and image.
    3. Navigates back to the inventory page after verifying each product's details.
    """

    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.assert_product_count(len(products))
    for i in range(len(products)):
        dashboard_page.click_on_product_and_verify_details(i, products[i])


def test_add_to_cart_and_remove_from_cart(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Clicks the "Add to Cart" button for the first product and verifies that the button text changes to "Remove" and the shopping cart badge updates to "1".
    3. Clicks the "Remove" button for the same product and verifies that the button text changes back to "Add to Cart" and the shopping cart badge is no longer visible.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()

    dashboard_page.click_on_add_to_cart_and_remove()


def test_all_products_cart_and_remove_functionality(login_as_standard_user):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Clicks the "Add to Cart" button for each product on the inventory page and verifies that the shopping cart badge updates to reflect the total number of items added.
    3. Clicks the "Remove" button for each product and verifies that the shopping cart badge updates accordingly, eventually disappearing when all items are removed.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()

    dashboard_page.assert_number_of_products()
    for _ in range(dashboard_page.get_inventory_items_count()):
        dashboard_page.click_add_to_cart()

    dashboard_page.assert_shopping_badge_value(dashboard_page.get_inventory_items_count())  

    for _ in range(dashboard_page.get_inventory_items_count()):
        dashboard_page.click_remove_button()

    dashboard_page.assert_shopping_badge_value(0)
