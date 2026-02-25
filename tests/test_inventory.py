import re
import pytest
from playwright.sync_api import Locator, expect
from pages.dashboard_page import DashboardPage
from test_data.product_data import PRODUCTS, allowed_cart
from test_data.filter_data import Filter


pytestmark = pytest.mark.inventory

@pytest.mark.smoke
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

@pytest.mark.smoke
def test_inventory_page_product_details(login_as_standard_user):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.assert_product_count(expected_count= len(PRODUCTS))
    dashboard_page.assert_product_visible(PRODUCTS, [])


@pytest.mark.parametrize(
        "product_index, product",
        [(index, product) for index, product in enumerate(PRODUCTS)],
        ids= [product.name for product in PRODUCTS]
        )
@pytest.mark.regression
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



@pytest.mark.parametrize("product_name", [product.name for product in PRODUCTS])
@pytest.mark.smoke
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


@pytest.mark.parametrize(
        "user",
        ["login_as_standard_user"],
        indirect=True
)
@pytest.mark.smoke
def test_all_products_cart_and_remove_functionality(user, add_all_products):
    """
    1. Logs in as a standard user and navigates to the inventory page.
    2. Clicks the "Add to Cart" button for each product on the inventory page and verifies that the shopping cart badge updates to reflect the total number of items added.
    3. Clicks the "Remove" button for each product and verifies that the shopping cart badge updates accordingly, eventually disappearing when all items are removed.
    """
    page, _ = add_all_products
    dashboard_page = DashboardPage(page)

    expected_cart_count = len(PRODUCTS)
    
    dashboard_page.assert_shopping_badge_value(expected_value=expected_cart_count)  

    for _ in range(dashboard_page.get_inventory_items_count()):
        dashboard_page.click_remove_button()

    dashboard_page.assert_shopping_badge_value(0)


@pytest.mark.slow
def test_product_images(login_as_standard_user, assert_snapshot, subtests):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)

    expected_count = len(PRODUCTS)

    for i in range(expected_count):
        # Change 2: Use the 'subtests' fixture here
        with subtests.test(msg=f"Product {i+1} image"):
            product_card = dashboard_page.inventory_items.nth(i)
            product_image = product_card.locator(dashboard_page.ITEM_IMG)
        
            ss = product_image.screenshot()
            assert_snapshot(ss, name=f"product_{i+1}_image.png")

@pytest.mark.slow
@pytest.mark.negative
def test_product_images_in_problem_user(login_as_problem_user, assert_snapshot, subtests):
    """
    1. Login as a problem user
    2. Assert if the product image is broken for all the products in inventory
    """
    page = login_as_problem_user
    dashboard_page = DashboardPage(page)

    expected_count = len(PRODUCTS)

    for i in range(expected_count):
        with subtests.test(msg=f"Product {i+1} image for problem user"):
            product_card = dashboard_page.inventory_items.nth(i)
            product_image = product_card.locator(dashboard_page.ITEM_IMG_DIV).first
        
            ss = product_image.screenshot()
            assert_snapshot(ss, name=f"dogesh.jpg")


@pytest.mark.parametrize(
    "user",
    [
        "login_as_problem_user",
        "login_as_error_user"
    ],
    indirect=True
)
@pytest.mark.negative
@pytest.mark.smoke
def test_other_user_add_and_remove_from_cart(user, request):
    '''
    1. For each users in user, Already on dashboard page
    2. iterate through all the products in inventory and try to add them to cart
    3. Assert if the expected items added to the cart and the others didn't
    '''
    
    page = user
    dashboard_page = DashboardPage(page)
    
    dashboard_page.wait_until_page_fields_are_ready()
    dashboard_page.assert_number_of_products()
    cart_count = 0 
    for product, isAllowed in allowed_cart.items():
        # add to cart
        dashboard_page.add_to_cart_by_product_name(product)
        
        # if allowed then remove button must appear
        remove_button = dashboard_page.get_remove_button_by_name(product)
        
        if(isAllowed):
            cart_count += 1
            expect(remove_button).to_be_visible()
            dashboard_page.assert_shopping_badge_value(cart_count)

        else :
            expect(remove_button).not_to_be_visible()
            dashboard_page.assert_shopping_badge_value(cart_count)



#concept : this parametrize will make a user --> "add_allowed_items" dependds on user fixture --> See if the user is created --> already created --> then This fixture will run and return us the allowed items added cart

@pytest.mark.parametrize(
        "user",
        [
            "login_as_problem_user",
            "login_as_error_user"
        ],
        indirect=True
)
@pytest.mark.smoke
@pytest.mark.negative
def test_remove_button_not_working(add_allowed_items):
    page = add_allowed_items
    dashboard_page = DashboardPage(page)

    added_items_cnt = 3

    for product, isAllowed in allowed_cart.items():
        remove_button = dashboard_page.get_remove_button_by_name(product_name=product)

        if isAllowed:
            #assuming the item is already added and works
            dashboard_page.remove_by_product_name(product_name=product)

            #remove should not work
            expect(remove_button).to_be_visible()
            dashboard_page.assert_shopping_badge_value(added_items_cnt)