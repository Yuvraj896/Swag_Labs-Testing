import re
import pytest
from typing import List
from playwright.sync_api import Locator, Page, expect
from test_data.product_data import products, Product
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class CheckoutPage :

    BURGER_MENU_FIELD = '.bm-burger-button > button'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'
    
    
    FIRST_NAME_FIELD = '[data-test="firstName"]'
    LAST_NAME_FIELD = '[data-test="lastName"]'
    ZIP_CODE_FIELD = '[data-test="postalCode"]'

    CHECKOUT_FIELD = '[data-test="title"]'

    CANCEL_BUTTON = '[data-test="cancel"]'
    CONTINUE_BUTTON = '[data-test="continue"]'

    CHECKOUT_URL = re.compile(r"step-one.html", re.I)
    ORDER_PAGE_URL = re.compile(r"step-two.html", re.IGNORECASE)

    ERROR_FIELD = '[data-test="error"]'

    def __init__(self, page : Page):
        self.page = page

    @property
    def checkout_text(self) -> Locator:
        return self.page.locator(self.CHECKOUT_FIELD).inner_text()
    
    @property
    def first_name(self) -> Locator:
        return self.page.locator(self.FIRST_NAME_FIELD)
    
    @property
    def zip_code(self) -> Locator:
        return self.page.locator(self.ZIP_CODE_FIELD)
    
    @property
    def last_name(self) -> Locator:
        return self.page.locator(self.LAST_NAME_FIELD)
    
    @property
    def continue_button(self) -> Locator:
        return self.page.locator(self.CONTINUE_BUTTON)
    
    @property
    def cancel_button(self) -> Locator:
        return self.page.locator(self.CANCEL_BUTTON)
    
    @property
    def burger_navigate_button(self) -> Locator:
        return self.page.locator(self.BURGER_MENU_FIELD)
    
    @property
    def shopping_cart(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_LINK)
    
    @property
    def shopping_cart_badge(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_BADGE)
    
    @property
    def shopping_cart_badge_value(self) -> int:
        badge = self.shopping_cart_badge
        if badge.count() == 0 : return 0
        return int(self.shopping_cart_badge.inner_text())

    @property
    def press_burger_menu(self) -> None:
        self.burger_navigate_button.click()

    @property
    def error_message(self) -> Locator:
        return self.page.locator(self.ERROR_FIELD)

    def is_checkout_page(self):
        expect(self.page).to_have_url(self.CHECKOUT_URL)

    
    def fill_details(self, first_name : str, last_name : str, zip_code : str):
        if not (first_name and last_name and zip_code) :
            raise ValueError(f"Details is not given")

        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.zip_code.fill(zip_code)


    def fill_form(self, first_name : str, last_name : str, zip_code : str) -> None:
        self.fill_details(first_name, last_name, zip_code)
        self.continue_button.click()    


