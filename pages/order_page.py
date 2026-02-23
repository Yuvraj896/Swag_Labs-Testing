import re
import pytest
from typing import List
from playwright.sync_api import Locator, Page, expect
from test_data.product_data import products, Product
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class OrderPage :

    BURGER_MENU_FIELD = '.bm-burger-button > button'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'

    OVERVIEW_FIELD = '[data-test="title"]'
    CART_LIST_FIELD = '[data-test="cart-list"]'
    INVENTORY_ITEMS  = f'{CART_LIST_FIELD} >> [data-test="inventory-item"]'
    ITEM_NAME_FIELD = '[data-test="inventory-item-name"]'
    ITEM_DESC_FIELD = '[data-test="inventory-item-desc"]'
    ITEM_PRICE_FIELD = '[data-test="inventory-item-price"]'

    PAYMENT_INFO = '[data-test="payment-info-label"]'
    SHIPPING_INFO = '[data-test="shipping-info-label"]'
    PRICE_TOTAL_FIELD = '[data-test="total-info-label"]'

    ITEM_TOTAL = '[data-test="subtotal-label"]'
    TAX_FIELD = '[data-test="tax-label"]'
    GRAND_TOTAL = '[data-test="total-label"]'

    FINISH_BUTTON_FIELD = '[data-test="finish"]'
    CANCEL_BUTTON_FIELD = '[data-test="cancel"]'

    URL = re.compile(r"two.html",re.I)

    def __init__(self, page : Page):
        self.page = page


    #------------Locators---------------

    @property
    def burger_navigate_button(self) -> Locator:
        return self.page.locator(self.BURGER_MENU_FIELD)
    
    @property
    def shopping_cart_link(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_LINK)
    
    @property
    def shopping_badge(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_BADGE)
    
    @property
    def checkout_overview(self) -> Locator:
        return self.page.locator(self.OVERVIEW_FIELD)
    
    @property
    def cart_list(self) -> Locator:
        return self.page.locator(self.CART_LIST_FIELD)
    
    @property
    def inventory_items(self) -> Locator:
        return self.page.locator(self.INVENTORY_ITEMS)
    
    @property
    def payment_info(self) -> Locator:
        return self.page.locator(self.PAYMENT_INFO)
    
    @property
    def ship_info(self) -> Locator:
        return self.page.locator(self.SHIPPING_INFO)
    
    @property
    def item_total(self) -> Locator:
        return self.page.locator(self.ITEM_TOTAL)
    
    @property
    def grand_total(self) -> Locator:
        return self.page.locator(self.GRAND_TOTAL)
    
    @property
    def tax(self) -> Locator:
        return self.page.locator(self.TAX_FIELD)
    
    @property
    def finish_button(self) -> Locator:
        return self.page.locator(self.FINISH_BUTTON_FIELD)
    
    @property
    def cancel_button(self) -> Locator:
        return self.page.locator(self.CANCEL_BUTTON_FIELD)
    
    @property
    def shopping_cart_badge_value(self) -> int:
        badge = self.shopping_badge
        if badge.count() == 0 : return 0
        return int(self.shopping_cart_badge.inner_text())
    
    @property
    def get_cart_items_count(self) -> int:
        return self.inventory_items.count()
    
    #---------------------Getter--------------
    
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

    def get_item_details(self, item_name = None, index= None) -> Locator:
        """
        Returns a dict containing the product details
        """

        item = self.get_inventory_item(item_name=item_name, index=index)        
        return {
            "name" : item.locator(self.ITEM_NAME_FIELD).inner_text(),
            "description" : item.locator(self.ITEM_DESC_FIELD).inner_text(),
            "price" : item.locator(self.ITEM_PRICE_FIELD).inner_text()
        }
    
    def get_item_price(self, item_name = None, index = None) -> float:
    
        item = self.get_inventory_item(item_name=item_name, index=index) 
        price = item.locator(self.ITEM_PRICE_FIELD).inner_text()  
        return float(price.replace("$", ""))
    #-------------------Asserts-----------------

    def is_order_page(self) -> None:
        expect(self.page).to_have_url(self.URL)

    def assert_fields_loaded(self) -> None:
        fields = (self.burger_navigate_button, self.shopping_cart_link, self.checkout_overview, self.cart_list, self.payment_info, self.ship_info, self.item_total, self.tax, self.grand_total)

        for field in fields:
            expect(field).to_be_visible()

    def assert_shopping_badge_value_equal_as_cart_cnt(self) -> None:
        cart_cnt = self.get_cart_items_count
        shopping_badge_cnt = self.shopping_cart_badge_value

        assert cart_cnt == shopping_badge_cnt, f"Expected {cart_cnt} , but found {shopping_badge_cnt}"

    def assert_no_of_items_in_cart(self, expected_cnt) -> None:
        actual_cnt = self.get_cart_items_count
        assert actual_cnt == expected_cnt, f"Expected {expected_cnt} products, but found {actual_cnt}"

    #--------------------Actions------------------
    def press_cancel_button(self) -> None:
        self.cancel_button.click()
    
    def press_finish_button(self) -> None:
        self.finish_button.click()
    

    def check_products_data(self, products_in_cart : List[Product]) -> None: 
        expected_count = len(products_in_cart)
        self.assert_no_of_items_in_cart(expected_count= expected_count)

        for product in products_in_cart:

            #find the product in inventory
            item_details = self.get_item_details(item_name=product.name)

            assert item_details["name"] == product.name, f"Name mismatch for {product.name}"
            assert item_details["description"] == product.description, f"Description mismatch for {product.name}"
            assert float(item_details["price"].replace("$", "")) == product.price, f"Price mismatch for {product.name}"

    def check_grand_total(self, products_in_cart : List[Product]) -> None:
        pass

