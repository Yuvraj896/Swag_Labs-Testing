import re
import pytest
from playwright.sync_api import Locator, expect
from pages.dashboard_page import DashboardPage
from test_data.product_data import products
from test_data.filter_data import Filter


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


def test_inventory_page_product_details(login_as_standard_user):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.assert_product_count(expected_count= len(products))
    dashboard_page.assert_product_visible(products, [])


@pytest.mark.parametrize(
        "product_index, product",
        [(index, product) for index, product in enumerate(products)],
        ids= [product.name for product in products]
        )
def test_each_product_page(login_as_standard_user, product_index, product):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Iterates through each product on the inventory page, clicks on it, and verifies that the product details page displays the correct name, description, price, and image.
    3. Navigates back to the inventory page after verifying each product's details.
    """

    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.click_on_product_and_verify_details(product_index, product)



@pytest.mark.parametrize("product_name", [product.name for product in products])
def test_add_to_cart_and_remove_from_cart(login_as_standard_user, product_name):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Clicks the "Add to Cart" button for the first product and verifies that the button text changes to "Remove" and the shopping cart badge updates to "1".
    3. Clicks the "Remove" button for the same product and verifies that the button text changes back to "Add to Cart" and the shopping cart badge is no longer visible.
    """
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()

    dashboard_page.wait_until_page_fields_are_ready()
    dashboard_page.add_to_cart_by_product_name(product_name)
    dashboard_page.assert_shopping_badge_value(1)
    dashboard_page.remove_by_product_name(product_name)
    dashboard_page.assert_shopping_badge_value(0)


def test_all_products_cart_and_remove_functionality(add_all_products):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Clicks the "Add to Cart" button for each product on the inventory page and verifies that the shopping cart badge updates to reflect the total number of items added.
    3. Clicks the "Remove" button for each product and verifies that the shopping cart badge updates accordingly, eventually disappearing when all items are removed.
    """
    page = add_all_products
    dashboard_page = DashboardPage(page)

    expected_cart_count = len(products)
    
    dashboard_page.assert_shopping_badge_value(expected_value=expected_cart_count)  

    for _ in range(dashboard_page.get_inventory_items_count()):
        dashboard_page.click_remove_button()

    dashboard_page.assert_shopping_badge_value(0)



def test_product_images(login_as_standard_user, assert_snapshot, subtests):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)

    expected_count = len(products)

    for i in range(expected_count):
        # Change 2: Use the 'subtests' fixture here
        with subtests.test(msg=f"Product {i+1} image"):
            product_card = dashboard_page.inventory_items.nth(i)
            product_image = product_card.locator(dashboard_page.ITEM_IMG)
        
            ss = product_image.screenshot()
            assert_snapshot(ss, name=f"product_{i+1}_image.png")
