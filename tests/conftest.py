import random
import re
import pytest

from config import URL
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from test_data.product_data import PRODUCTS, allowed_cart

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def login(page):
    def login_user(username: str, password: str = "secret_sauce", url = URL) :
        login_page = LoginPage(page)
        login_page.open_and_login(url, username, password)
        return page

    return login_user


@pytest.fixture(scope="function")
def login_as_standard_user(login):
    return login("standard_user")

@pytest.fixture(scope="function")
def login_as_problem_user(login):
    return login("problem_user")

@pytest.fixture(scope="function")
def login_as_visual_user(login):
    return login("visual_user")

@pytest.fixture(scope="function")
def login_as_locked_out_user(login):
    return login("locked_out_user")

@pytest.fixture(scope="function")
def login_as_error_user(login):
    return login("error_user")


@pytest.fixture(scope="function")
def add_no_products(user):
    page = user
    return page, []



@pytest.fixture(scope="function")
def add_all_products(user):
    page = user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.wait_until_page_fields_are_ready()
    
    for product in PRODUCTS:
        dashboard_page.add_to_cart_by_product_name(product.name)

    return page, PRODUCTS


@pytest.fixture(scope="function")
def add_some_products(user):
    page = user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.wait_until_page_fields_are_ready()
    
    random_products = random.sample(PRODUCTS, 3)  # Select 3 random products    

    for product in random_products:
        dashboard_page.add_to_cart_by_product_name(product.name)

    return page, random_products


@pytest.fixture
def add_allowed_items(user):
    page = user
    dashboard_page = DashboardPage(page)
    dashboard_page.wait_until_page_fields_are_ready()

    for product, isAllowed in allowed_cart.items():
        if isAllowed:
            dashboard_page.add_to_cart_by_product_name(product_name=product)

    return page

# cart_state fixture resolves the cart content
@pytest.fixture
def cart_state(request):
    if hasattr(request, "param"):
        return request.getfixturevalue(request.param)

    return request.getfixturevalue("add_no_products")


# user fixture that resolves a login
@pytest.fixture
def user(request):
    if hasattr(request, "param"):
        return request.getfixturevalue(request.param)
    
    return request.getfixturevalue("login_as_standard_user")


#--------------------_For Cart Page------------------

#this fixture just make sure you have a cart state and move to cart page
@pytest.fixture
def cart_page_with_products(cart_state):
    page, added_products = cart_state
    DashboardPage(page).open_cart_page()
    return page, added_products

@pytest.fixture
def cart_page_navigate(user):
    page = user
    DashboardPage(page).open_cart_page()
    return page


#--------------------For checkout page-----------------

@pytest.fixture
def checkout_page_navigate(cart_page_navigate):
    page = cart_page_navigate       
    CartPage(page).checkout_button.click()
    CheckoutPage(page).is_checkout_page()
    return page


@pytest.fixture(autouse=True)
def show_browser(browser_name):
    print(f"\n=== Running on {browser_name.upper()} ===")


#-----------------For Order page-----------------
@pytest.fixture
def order_page_navigate(cart_page_with_products):
    page, added_products = cart_page_with_products
    CartPage(page).checkout_button.click()
    checkout_page = CheckoutPage(page)
    checkout_page.is_checkout_page()
    checkout_page.fill_form_and_continue()
    
    return page, added_products




