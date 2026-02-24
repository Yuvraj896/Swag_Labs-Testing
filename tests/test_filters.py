import re
import time
from typing import List
import pytest
from playwright.sync_api import Locator, expect, Page
from pages.dashboard_page import DashboardPage
from test_data.product_data import  Product, products
from test_data.filter_data import Filter

#-----------------Parametrize over cart_state and filter_option --> Indirect param -----------------
pytestmark = pytest.mark.filters



@pytest.mark.parametrize(
    "cart_state", 
    [
        "add_no_products",
        "add_some_products",
        "add_all_products"
    ],
    indirect=True
)
@pytest.mark.parametrize(
    "filter_option",
    list(Filter)[1:]
)
@pytest.mark.regression
def test_filter_behaviour(cart_state, filter_option):
    page, added_products = cart_state
    
    dashboard_page = DashboardPage(page)
    dashboard_page.apply_filter(filter_option=filter_option)
    sorted_products = Product.sort_products(products, filter_option)
    dashboard_page.assert_product_visible(products=sorted_products, added_products=added_products)


@pytest.mark.parametrize(
    "filter_option",
    list(Filter)[1:]
)
@pytest.mark.negative
@pytest.mark.regression
def test_problem_user_filter(login_as_problem_user, filter_option):
    page = login_as_problem_user
    dashboard_page = DashboardPage(page)
    dashboard_page.apply_filter(filter_option=filter_option)

    dashboard_page.assert_filter_applied(expected_filter= filter_option)
    dashboard_page.filter_behaviour_on_problem_user(products= products)
    

@pytest.mark.parametrize(
    "filter_option",
    list(Filter)[1:]
)
@pytest.mark.negative
@pytest.mark.regression
def test_error_user_filter(login_as_error_user, filter_option):
    """
    1. Login as Error user
    2. Applies filter as filter_option
    3. Assert if the dialog pop up appeared
    4. Assert if the filter option changed in the UI
    """
    
    page = login_as_error_user
    dashboard_page = DashboardPage(page)

    dashboard_page.dialog_message = None

    
    # add a method in the dashboard class to handle dialogs
    page.on("dialog", dashboard_page.handle_dialog )
    dashboard_page.apply_filter(filter_option=filter_option)
    
    assert dashboard_page.dialog_message is not None
    dashboard_page.assert_filter_applied(expected_filter= filter_option)
