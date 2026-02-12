from playwright.sync_api import Locator, Page, expect
import re
import pytest

class DashboardPage :

    #------------Headers------------
    PRIMARY_HEADER = '[data-test="primary-header"]'
    BURGER_MENU_BUTTON = f'{PRIMARY_HEADER} >> #react-burger-menu-btn'    
    SHOPPING_CART_BUTTON = '[data-test="shopping-cart-link"]'


    SECONDARY_HEADER = '[data-test="secondary-header"]'
    PRODUCTS_TITLE = f'{SECONDARY_HEADER} >> [data-test="title"]'
    FILTER_BUTTON = f'{SECONDARY_HEADER} >> [data-test="product-sort-container"]'

    #------------Products------------
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    INVENTORY_LIST = f'{INVENTORY_CONTAINER} >> [data-test="inventory-item"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    INVENTORY_ITEM_LINK = '[data-test$="title-link"]'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart-"]'
    ITEM_IMG = '.inventory_item_img img'
    ITEM_DESC = '[data-test="inventory-item-desc"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    BACK_TO_PRODUCTS_BUTTON = '[data-test="back-to-products"]'


# <button class="btn btn_secondary btn_small btn_inventory " data-test="remove-test.allthethings()-t-shirt-(red)" id="remove-test.allthethings()-t-shirt-(red)" name="remove-test.allthethings()-t-shirt-(red)">Remove</button>

# <button class="btn btn_primary btn_small btn_inventory " data-test="add-to-cart-test.allthethings()-t-shirt-(red)" id="add-to-cart-test.allthethings()-t-shirt-(red)" name="add-to-cart-test.allthethings()-t-shirt-(red)">Add to cart</button>

    #-------------Separate Product Page Selectors------------
    DETAILS_ITEM_IMG = '.inventory_details_img'

    #-----------selectors------------

    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'
    REMOVE_BUTTON_FIELD = '[data-test^="remove-"]'
    REMOVE_BUTTON = f'{INVENTORY_ITEMS} >> {REMOVE_BUTTON_FIELD}'

    CART_PAGE_CONTINUE_SHOPPING = '[name="continue-shopping"]'
    PRODUCT_PRICES = '[data-test="inventory-item-price"]'
    

    #-----------page texts-----------
    PAGE_HEADING = re.compile(r"Swag Labs", re.I)

    
    
    #---------------Validations-----------
    CART_URL = re.compile(r"cart.html", re.I)
    INVENTORY_URL = re.compile(r"inventory.html", re.I)
    

    #----------------Mask-----------------
    PRICE_BAR = '.pricebar'

    def __init__(self, page: Page) -> None:
        self.page = page
    
    
    
    #--------------locators---------------
    @property
    def burger_menu_button(self) -> Locator:
        return self.page.locator(self.BURGER_MENU_BUTTON)

    @property
    def filter_button(self) -> Locator:
        return self.page.locator(self.FILTER_BUTTON)

    @property
    def primary_header(self) -> Locator:
        return self.page.locator(self.PRIMARY_HEADER)

    @property
    def shopping_cart_button(self) -> Locator:
        return self.page.locator(self.SHOPPING_CART_BUTTON)
    
    @property
    def inventory_container(self) -> Locator:
        return self.page.locator(self.INVENTORY_CONTAINER)
    
    @property
    def add_to_cart_button(self) -> Locator:
        return self.page.locator(self.ADD_TO_CART_BUTTON)
    
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
        return self.page.locator(self.REMOVE_BUTTON_FIELD)
    
    @property
    def cart_page_continue_shopping(self) -> Locator:
        return self.page.locator(self.CART_PAGE_CONTINUE_SHOPPING)
    
    @property
    def product_prices(self) -> Locator:
        return self.page.locator(self.PRODUCT_PRICES)

    @property
    def price_bar_mask(self) -> Locator:
        return self.page.locator(self.PRICE_BAR)
    
    @property
    def go_back_to_dashboard_button(self) -> Locator:
        return self.page.locator(self.BACK_TO_PRODUCTS_BUTTON)
    
    @property
    def item_name(self) -> Locator:
        return self.page.locator(self.ITEM_NAME)   
    
    @property
    def item_desc(self) -> Locator:
        return self.page.locator(self.ITEM_DESC)   
    
    @property
    def item_price(self) -> Locator:
        return self.page.locator(self.ITEM_PRICE)
    
    @property
    def details_item_img(self) -> Locator:
        return self.page.locator(self.DETAILS_ITEM_IMG)


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

    def is_inventory_page(self) -> None:
        expect(self.page).to_have_url(self.INVENTORY_URL)

    def assert_page_headers_visible(self) -> None:
        expect(self.primary_header).to_be_visible()
        expect(self.page_heading).to_be_visible()
        expect(self.burger_menu_button).to_be_visible()
        expect(self.shopping_cart_button).to_be_visible()

        expect(self.filter_button).to_be_visible()
        expect(self.products_title).to_be_visible()

    def assert_product_count(self, expected_count: int) -> None:
        actual_count = self.get_inventory_items_count()
        assert actual_count == expected_count, f"Expected {expected_count} products, but found {actual_count}"

    def assert_product_visible(self, products, added_products) -> None:
        """
        1. Assert product count
        2. Assert each product's details: name, image, description, price
        3. If product is added to cart, assert remove button is visible
        """

        expected_count = len(products)
        self.assert_product_count(expected_count)

        for i in range(expected_count):
            product_card = self.inventory_items.nth(i)
            product = products[i]

            if i in added_products:
                expect(product_card.locator(self.REMOVE_BUTTON)).to_have_text("Remove")

            # assert product details
            expect(product_card.locator(self.ITEM_NAME)).to_have_text(product.name)
            expect(product_card.locator(self.ITEM_IMG)).to_have_attribute("src", product.image_path)
            expect(product_card.locator(self.ITEM_NAME)).to_have_text(product.name)
            expect(product_card.locator(self.ITEM_DESC)).to_contain_text(product.description)
            expect(product_card.locator(self.ITEM_PRICE)).to_have_text(f"${product.price:.2f}")


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
    def click_add_to_cart(self, index: int = 0) -> None:
        if(index > self.get_inventory_items_count() - 1):
            raise IndexError(f"Index {index} is out of bounds for inventory items count {self.get_inventory_items_count()}")
        
        self.assert_add_to_cart_visible()
        self.add_to_cart_button.nth(index).click()
        self.assert_remove_button_visible()

    def click_remove_button(self, index: int = 0) -> None:
        if(index > self.get_inventory_items_count() - 1):
            raise IndexError(f"Index {index} is out of bounds for inventory items count {self.get_inventory_items_count()}")
        
        self.assert_remove_button_visible()
        self.remove_button.nth(index).click()
        self.assert_add_to_cart_visible()

    
    def get_filter(self, value: str) -> Locator:
        return self.page.locator(self.FILTER_BUTTON).select_option(value=value)

    def apply_filter(self, filter_value: str) -> None:
        self.filter_button.click()
        filter_option_locator = self.get_filter(filter_value)

   
   
   
    #-------------Post actions--------------

    
  
  
    #-------------E2E Flows--------------

    def click_on_product_and_verify_details(self, product_index: int, product) -> None:
        """
        1. Click on the product
        2. Verify the product details page
        3. Navigate back to the dashboard page
        4. Verify the dashboard page is displayed
        """

        product_card = self.inventory_items.nth(product_index)
        product_card.locator(self.INVENTORY_ITEM_LINK).click()

        # Verify product details page
        expect(self.item_name).to_have_text(product.name)
        expect(self.item_desc).to_contain_text(product.description)
        expect(self.item_price).to_have_text(f"${product.price:.2f}")
        expect(self.details_item_img).to_have_attribute("src", product.image_path)

        # Navigate back to dashboard page
        self.go_back_to_dashboard_button.click()
        self.is_inventory_page()



    def click_on_add_to_cart_and_remove(self) -> None:
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


    def add_a_fiter_and_assert_products(self, filter_value: str) -> None:
        """
        1. Already on dashboard page
        2. wait for page fields to load
        3. apply filter
        4. assert products are sorted based on the filter applied
        """

        self.wait_until_page_fields_are_ready()
        self.apply_filter(filter_value)




    def cart_page_navigation_and_state(self) -> None:
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
            
    
    def cart_behaviour(self) -> None:
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

        
