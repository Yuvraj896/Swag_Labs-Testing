import re
import pytest
from typing import List
from playwright.sync_api import Locator, Page, expect
from test_data.product_data import PRODUCTS, Product
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class CartPage:
    #-----------Headers--------------
    YOUR_CART_FIELD = '[data-test="title"]'
    BURGER_MENU_FIELD = '.bm-burger-button > button'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'

    #-----------Selectors-------------
    CART_LIST_FIELD = '[data-test="cart-list"]'
    QTY_FIELD = f'{CART_LIST_FIELD} >> [data-test="cart-quantity-label"]'
    DESCRIPTION_FIELD = f'{CART_LIST_FIELD} >> [data-test="cart-desc-label"]'

    #will select mutliple inventory items
    INVENTORY_ITEMS  = f'{CART_LIST_FIELD} >> [data-test="inventory-item"]'
    ITEM_NAME_FIELD = '[data-test="inventory-item-name"]'
    ITEM_DESC_FIELD = '[data-test="inventory-item-desc"]'
    ITEM_PRICE_FIELD = '[data-test="inventory-item-price"]'
    REMOVE_BUTTON_FIELD = '[data-test^="remove-"]'

    #------------Footer----------------
    CART_FOOTER_FIELD = '.cart_footer'
    CONTINUE_SHOPPING_FIELD = f'{CART_FOOTER_FIELD} >> [data-test="continue-shopping"]'
    CHECKOUT_FIELD = f'{CART_FOOTER_FIELD} >> [data-test="checkout"]'

    #----------Validations-----------
    CART_URL = re.compile(r"cart.html", re.I)
    PAGE_HEADING = re.compile(r"Swag Labs", re.I)

    #----------Navigation buttons---------
    LOGOUT_FIELD = '[data-test="logout-sidebar-link"]'
    

    
    def __init__(self, page: Page):
        self.page = page

    #----------Locators-------------

    @property
    def page_heading(self) -> Locator:
        return self.page.get_by_text(self.PAGE_HEADING)

    @property
    def burger_navigate_button(self) -> Locator:
        return self.page.locator(self.BURGER_MENU_FIELD)

    @property
    def your_cart(self) -> Locator:
        return self.page.locator(self.YOUR_CART_FIELD)
    
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
    def cart_list(self) -> Locator:
        return self.page.locator(self.CART_LIST_FIELD)
    
    @property
    def quantity_column(self) -> Locator:
        return self.page.locator(self.QTY_FIELD)

    @property
    def get_cart_items_count(self) -> int:
        return self.inventory_items.count()
    
    @property
    def description_col(self) -> Locator:
        return self.page.locator(self.DESCRIPTION_FIELD)

    @property
    def inventory_items(self) -> Locator:
        return self.page.locator(self.INVENTORY_ITEMS)

    @property
    def cart_footer(self) -> Locator:
        return self.page.locator(self.CART_FOOTER_FIELD)

    @property
    def continue_shopping_button(self) -> Locator:
        return self.page.locator(self.CONTINUE_SHOPPING_FIELD)
    
    @property
    def checkout_button(self) -> Locator:
        return self.page.locator(self.CHECKOUT_FIELD)
    
    @property
    def logout_button(self) -> Locator:
        return self.page.locator(self.LOGOUT_FIELD)
    
    @property
    def is_cart_empty(self) -> bool:
        return self.get_cart_items_count == 0
    
    @property
    def press_checkout_button(self) -> None:
        self.checkout_button.click()
    
    @property
    def press_continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    @property
    def press_burger_menu(self) -> None:
        self.burger_navigate_button.click()


    #----------Getters------------
    def get_inventory_item(self, item_name = None , index = None) -> Locator:
        """
        Return a locator of inventory Item of the required item
        """
        if self.is_cart_empty:
            raise AssertionError("Cart is empty, No Inventory items found")

        if item_name:
            item = self.inventory_items.filter(has_text=item_name)
            if item.count() == 0:
                raise ValueError(f"Item with name '{item_name}' not found in the cart")
            return item
        
        if index is not None:
            if index >= self.get_cart_items_count:
                raise ValueError("Item index out of range")
            return self.inventory_items.nth(index)

        else :
            raise ValueError("Either item_name or index must be provided")
        

    def get_item_details(self, item_name = None, index= None) -> dict:
        """
        Returns a dict containing the product details
        """

        item = self.get_inventory_item(item_name=item_name, index=index)        
        return {
            "name" : item.locator(self.ITEM_NAME_FIELD).inner_text(),
            "description" : item.locator(self.ITEM_DESC_FIELD).inner_text(),
            "price" : item.locator(self.ITEM_PRICE_FIELD).inner_text()
        }

    def remove_button(self, item_name = None , index = None) -> Locator:
        return self.get_inventory_item(item_name, index).locator(self.REMOVE_BUTTON_FIELD)

    #---------------assertions------------------

    def is_cart_page(self) -> None:
        expect(self.page).to_have_url(self.CART_URL)


    def assert_product_count_in_cart(self, expected_count) -> None:
        actual_cnt = self.get_cart_items_count
        assert actual_cnt == expected_count, f"Expected {expected_count} products, but found {actual_cnt}"

    
    def assert_shopping_badge_value_equal_as_cart_cnt(self) -> None:
        cart_cnt = self.get_cart_items_count
        shopping_badge_cnt = self.shopping_cart_badge_value

        assert cart_cnt == shopping_badge_cnt, f"Expected {cart_cnt} , but found {shopping_badge_cnt}"
    

    #---------------actions--------------------
    def press_remove_button(self, item_name = None , index = None) -> None:
        remove_button = self.remove_button(item_name=item_name, index=index)
        remove_button.click()

    def press_logout_button(self) -> None:
        self.press_burger_menu
        self.logout_button.click()
    
    
    def press_remove_button_and_assert_badge_count(self, item_name = None, index = None) -> None:
        current_cnt = self.shopping_cart_badge_value
        self.press_remove_button(item_name=item_name, index=index)
        self.assert_product_count_in_cart(expected_count=current_cnt-1)
        self.assert_shopping_badge_value_equal_as_cart_cnt()

    def check_headers(self) -> None:
        self.is_cart_page()
        expect(self.page_heading).to_be_visible()
        expect(self.burger_navigate_button).to_be_visible()
        expect(self.shopping_cart).to_be_visible()
        expect(self.your_cart).to_be_visible()

    def check_body_and_footers(self) -> None:
        expect(self.cart_list).to_be_visible()
        expect(self.continue_shopping_button).to_be_visible()
        expect(self.checkout_button).to_be_visible()
    
    #-----------------E2E Flow-------------------

    def check_page_locators_visibility(self) -> None:
        self.check_headers()
        self.check_body_and_footers()


    def check_products_data(self, products_in_cart : List[Product]) -> None: 
        expected_count = len(products_in_cart)
        self.assert_product_count_in_cart(expected_count= expected_count)

        for product in products_in_cart:

            #find the product in inventory
            item_details = self.get_item_details(item_name=product.name)

            assert item_details["name"] == product.name, f"Name mismatch for {product.name}"
            assert item_details["description"] == product.description, f"Description mismatch for {product.name}"
            assert float(item_details["price"].replace("$", "")) == product.price, f"Price mismatch for {product.name}"

    def relogin_and_navigate_to_cart_page(self, username: str = "standard_user", password : str = "secret_sauce"):
        self.press_logout_button()
        LoginPage(self.page).login(username, password)
        DashboardPage(self.page).open_cart_page()
        self.is_cart_page()

