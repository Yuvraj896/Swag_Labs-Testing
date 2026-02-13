import random
import re
import pytest

from config import URL
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from test_data.product_data import products

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
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
def add_all_products(login_as_standard_user):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.wait_until_page_fields_are_ready()
    
    for product in products:
        dashboard_page.add_to_cart_by_product_name(product.name)

    return page


@pytest.fixture(scope="function")
def add_some_products(login_as_standard_user):
    page = login_as_standard_user
    dashboard_page = DashboardPage(page)
    dashboard_page.is_inventory_page()
    dashboard_page.wait_until_page_fields_are_ready()
    
    random_products = random.sample(products, 3)  # Select 3 random products    

    for product in random_products:
        dashboard_page.add_to_cart_by_product_name(product.name)

    return page, random_products