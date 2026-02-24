import re
import time
from typing import List
import pytest
from playwright.sync_api import Locator, expect, Page
from pages.dashboard_page import DashboardPage
from pages.checkout_page import CheckoutPage
from test_data.product_data import  Product, products
from test_data.filter_data import Filter

pytestmark = pytest.mark.checkout

#---------remove param , -> Login as st user----------
@pytest.mark.parametrize(
        "user",
        ["login_as_standard_user"],
        indirect=True
)
@pytest.mark.smoke
def test_checkout_success(checkout_page_navigate, user):
    page = checkout_page_navigate
    checkout_page = CheckoutPage(page)

    checkout_page.fill_form_and_continue(
        first_name="Jon",
        last_name="Snow",
        zip_code="123"
    )

    expect(page).to_have_url(checkout_page.ORDER_PAGE_URL)

@pytest.mark.parametrize(
    "user",
    ["login_as_standard_user"],
    indirect=True
)
@pytest.mark.parametrize("first,last,zip_code", [
    ("", "Doe", "12345"),
    ("John", "", "12345"),
    ("John", "Doe", ""),
])
@pytest.mark.negative
def test_checkout_validation_errors(checkout_page_navigate, first, last, zip_code, user):
    checkout_page = CheckoutPage(checkout_page_navigate)

    checkout_page.first_name.fill(first)
    checkout_page.last_name.fill(last)
    checkout_page.zip_code.fill(zip_code)

    checkout_page.continue_button.click()

    expect(checkout_page.error_message).to_be_visible()

