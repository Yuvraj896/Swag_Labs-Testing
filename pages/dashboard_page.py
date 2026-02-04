from playwright.sync_api import Locator, Page, expect
import re
import pytest

class DashboardPage :

    #-----------selectors------------
    SHOPPING_CART_BUTTON = '[data-test="shopping-cart-link"]'
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart-"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    REMOVE_BUTTON_FIELD = '[data-test^="remove-"]'

    CART_PAGE_CONTINUE_SHOPPING = '[name="continue-shopping"]'
    PRODUCT_PRICES = '[data-test="inventory-item-price"]'
    


    #-----------page texts-----------
    PAGE_HEADING = re.compile(r"Swag Labs", re.I)
    PRODUCTS_TITLE = '[data-test="title"]'

    
    
    #---------------Validations-----------
    CART_URL = re.compile(r"cart.html", re.I)
    

    #----------------Mask-----------------
    PRICE_BAR = '.pricebar'

    def __init__(self, page: Page) -> None:
        self.page = page
    
    
    
    #--------------locators---------------
    @property
    def shopping_cart_button(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_BUTTON)
    
    @property
    def inventory_container(self) -> Locator:
        return self.page.locator(self.INVENTORY_CONTAINER)
    
    @property
    def add_to_cart_button(self) -> Locator:
        return self.page.locator(self.ADD_TO_CART_BUTTON).first
    
    @property
    def shopping_cart_badge(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_BADGE)
    
    @property
    def page_heading(self) -> Locator:
        return self.page.get_by_text(self.PAGE_HEADING)
    
    @property
    def products_title(self)  -> Locator:
        return self.page.locator(self.PRODUCTS_TITLE)
   
    @property
    def inventory_items(self) -> Locator:
        return self.page.locator(self.INVENTORY_ITEMS)

    @property
    def remove_button(self) -> Locator:
        return self.page.locator(self.REMOVE_BUTTON_FIELD).first
    
    @property
    def cart_page_continue_shopping(self) -> Locator:
        return self.page.locator(self.CART_PAGE_CONTINUE_SHOPPING)
    
    @property
    def product_prices(self) -> Locator:
        return self.page.locator(self.PRODUCT_PRICES)

    @property
    def price_bar_mask(self) -> Locator:
        return self.page.locator(self.PRICE_BAR)

    #-------------Helper----------------
    def get_inventory_items_count(self) -> int:
        return self.inventory_items.count()


    #-------------navigations--------------
    def open_cart(self) -> None :
        self.shopping_cart_button.click()
        self.assert_cart_page()

    def open_dashboard_page_from_cart_page(self) -> None:
        self.cart_page_continue_shopping.click()
        self.wait_until_page_fields_are_ready()
        
    #-------------assertions--------------
    def wait_until_page_fields_are_ready(self) -> None:
        fields = (self.page_heading, self.products_title, self.shopping_cart_button, self.inventory_container)

        for field in fields:
            expect(field).to_be_visible()

    def assert_number_of_products(self) -> None :
        count = self.get_inventory_items_count()
        assert count == 6, f"Expected 6 products, but found {count}"
   
    def assert_remove_button_visible(self) -> None:
        assert self.remove_button.is_visible(), "Remove button is not visible"

    def assert_add_to_cart_visible(self) -> None:
        assert self.add_to_cart_button.is_visible(), "Add to cart button is not visible"

    def assert_shopping_badge_value(self, expected_value: int) -> None:
        badge = self.shopping_cart_badge
        if expected_value == 0:
            expect(badge).to_have_count(0)
        
        else :
            expect(badge).to_be_visible()
            expect(badge).to_have_text(str(expected_value))

    def assert_cart_page(self) -> None:
        expect(self.page).to_have_url(self.CART_URL)

    
 
    #--------------actions---------------
    def click_add_to_cart(self):
        self.assert_add_to_cart_visible()
        self.add_to_cart_button.click()
        self.assert_shopping_badge_value(1)
        self.assert_remove_button_visible()

    def click_remove_button(self):
        self.assert_remove_button_visible()
        self.remove_button.click()
        self.assert_shopping_badge_value(0)
        self.assert_add_to_cart_visible()


   
   
   
    #-------------Post actions--------------

    
  
  
    #-------------E2E Flows--------------
    def standard_user_shopping_elements(self) -> None:
        """
        1. Already on dashboard page
        2. Wait until the page fields are visible 
        4. Click on add to cart button
        3. Check if the products = 6
        5. Check the shopping card badge
        6. Click on remove button
        7. Checks the shopping card badge 
        """

        self.wait_until_page_fields_are_ready()
        self.assert_number_of_products()
        self.click_add_to_cart()
        self.click_remove_button()


    def standard_user_cart_page_navigation_and_state(self) -> None:
        """
        1. Already on dashboard page
        2. Wait until the page fields are visible
        3. Add two items into the cart
        4. navigate to cart page
        5. navigate back to dashboard page
        6. check dashboard page state changes
        """

        self.wait_until_page_fields_are_ready()
        self.click_add_to_cart()
        self.open_cart()
        self.open_dashboard_page_from_cart_page()
        self.assert_shopping_badge_value(1)

    
    def problem_user_verify_broken_image(self) -> None:
        """
        1. Already on dashboard page
        2. Wait until the page fields are visible
        3. Verify broken image for problem user
        """

        self.wait_until_page_fields_are_ready()
        
        try: 
            self.assert_number_of_products()
        except AssertionError :
            print("Inventory count mismatch detected for problem_user")
        
        for idx , item in enumerate(self.inventory_items.all()):
            img_src = item.locator("img").get_attribute("src")

            if "sl-404" in img_src :
                print(f"Broken image at product {idx + 1}")
            
    
    def problem_user_cart_behaviour(self) -> None:
        """
        1. Already on dashboard page
        2. wait for page fields to load
        3. add product to cart
        4. check badge increment
        5. try removing product
        6. log if remove button won't work
        """

        self.wait_until_page_fields_are_ready()
        try: 
            self.click_add_to_cart()
        except AssertionError as e:
            print ("Add to cart failed for problem_user:", e)
        
        try:
            self.click_remove_button()
        except AssertionError as e:
            print("Remove button failed for problem_user:", e)

        
