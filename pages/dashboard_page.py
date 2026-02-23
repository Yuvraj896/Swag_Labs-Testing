from playwright.sync_api import Locator, Page, expect
import re

class DashboardPage :

    #------------Headers------------
    PRIMARY_HEADER = '[data-test="primary-header"]'
    BURGER_MENU_BUTTON = f'{PRIMARY_HEADER} >> #react-burger-menu-btn'    
    SHOPPING_CART_BUTTON = '[data-test="shopping-cart-link"]'
    LOGOUT_BUTTON = f'{PRIMARY_HEADER} >> #logout_sidebar_link'



    SECONDARY_HEADER = '[data-test="secondary-header"]'
    PRODUCTS_TITLE = f'{SECONDARY_HEADER} >> [data-test="title"]'
    FILTER_BUTTON = f'{SECONDARY_HEADER} >> [data-test="product-sort-container"]'
    CURRENT_FILTER = f'{FILTER_BUTTON} >> .active_option'

    #------------Products------------
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    INVENTORY_LIST = f'{INVENTORY_CONTAINER} >> [data-test="inventory-item"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    INVENTORY_ITEM_LINK = '[data-test$="title-link"]'
    ADD_TO_CART_BUTTON = f'{INVENTORY_ITEMS} >> [data-test^="add-to-cart-"]'
    ADD_TO_CART_BUTTON_FIELD = '[data-test^="add-to-cart-"]'
    ITEM_IMG = '.inventory_item_img img'
    ITEM_DESC = '[data-test="inventory-item-desc"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    BACK_TO_PRODUCTS_BUTTON = '[data-test="back-to-products"]'
    ITEM_IMG_DIV = '.inventory_item_img'

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
    
    @property
    def logout_button(self) -> Locator:
        return self.page.locator(self.LOGOUT_BUTTON)

    @property
    def active_filter(self) -> Locator:
        return self.page.locator(f'{self.FILTER_BUTTON} option:checked')

    #-------------Helper----------------
    def get_inventory_items_count(self) -> int:
        return self.inventory_items.count()
    
    def get_add_to_cart_button(self, index: int) -> Locator:
        return self.page.locator(self.ADD_TO_CART_BUTTON).nth(index)
    
    def get_remove_button(self, index: int) -> Locator:
        return self.page.locator(self.REMOVE_BUTTON).nth(index)
    
    def get_remove_button_by_name(self, product_name) -> None:
        product_card = self.inventory_items.filter(has_text=product_name)
        remove_button = product_card.locator(self.REMOVE_BUTTON_FIELD)
        return remove_button

    #-------------navigations--------------
    def open_cart_page(self) -> None :
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

    def wait_until_page_fields_are_ready(self) -> None:
        fields = (self.page_heading, self.products_title, self.shopping_cart_button, self.inventory_container)

        for field in fields:
            expect(field).to_be_visible()

    def assert_number_of_products(self) -> None :
        count = self.get_inventory_items_count()
        assert count == 6, f"Expected 6 products, but found {count}"
   
    def assert_remove_button_visible(self, index: int = 0) -> None:
        assert self.get_remove_button(index).is_visible(), f"Remove button for product at index {index} is not visible"

    def assert_add_to_cart_visible(self, index: int = 0) -> None:
        assert self.get_add_to_cart_button(index).is_visible(), f"Add to cart button for product at index {index} is not visible"

    def assert_shopping_badge_value(self, expected_value: int) -> None:
        badge = self.shopping_cart_badge
        if expected_value == 0:
            expect(badge).to_have_count(0)
        
        else :
            expect(badge).to_be_visible()
            expect(badge).to_have_text(str(expected_value))

    def assert_cart_page(self) -> None:
        expect(self.page).to_have_url(self.CART_URL)

    def assert_filter_applied(self, expected_filter: str) -> None:
        selected_option = self.active_filter.inner_text()

        try :
            assert selected_option == expected_filter, f"Expected filter option '{expected_filter}' to be applied, but found '{selected_option}'"

        except AssertionError as e:
            print("Filter application assertion failed:", e)
    

 
    #--------------actions---------------
    def click_add_to_cart(self, index: int = 0) -> None:
        if(index > self.get_inventory_items_count() - 1):
            raise IndexError(f"Index {index} is out of bounds for inventory items count {self.get_inventory_items_count()}")
        
        self.assert_add_to_cart_visible(index)
        self.get_add_to_cart_button(index).click()
        self.assert_remove_button_visible()

    def click_remove_button(self, index: int = 0) -> None:
        if(index > self.get_inventory_items_count() - 1):
            raise IndexError(f"Index {index} is out of bounds for inventory items count {self.get_inventory_items_count()}")
        
        self.assert_remove_button_visible()
        self.get_remove_button(index).click()   
        self.assert_add_to_cart_visible(index)
    
    def get_filter(self, option: str) -> Locator:
        return self.page.locator(self.FILTER_BUTTON).select_option(label=option)

    def apply_filter(self, filter_option: str) -> None:
        self.filter_button.click()
        filter_option_locator = self.get_filter(filter_option.value)

    def add_to_cart_by_product_name(self, product_name: str) -> None:
        product_card = self.inventory_items.filter(has_text=product_name)
        add_button = product_card.locator(self.ADD_TO_CART_BUTTON_FIELD)
        expect(add_button).to_be_visible()
        add_button.click()

    def remove_by_product_name(self, product_name: str) -> None:
        product_card = self.inventory_items.filter(has_text=product_name)
        remove_button = product_card.locator(self.REMOVE_BUTTON_FIELD)
        expect(remove_button).to_be_visible()
        remove_button.click()


    def logout(self) -> None:
        self.burger_menu_button.click()
        self.logout_button.click()


    #-------------Post actions--------------

    def handle_dialog(self, dialog):
        self.dialog_message = dialog.message
        dialog.accept()
  
  
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
        self.open_cart_page()
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


    def filter_behaviour_on_problem_user(self, products) -> None:
        """
        1. Assert Product count
        2. Assert Filter sorting didn't worked for problem_user
        3. Check The product details
        """
        expected_count = len(products)
        
        for i in range(expected_count):
            product_card = self.inventory_items.nth(i)
            product = products[i]

            expect(product_card.locator(self.ITEM_NAME)).to_have_text(product.name)

            expect(product_card.locator(self.ITEM_IMG)).to_have_attribute("src", re.compile(r"sl-404", re.I))



    def assert_product_visible(self, products, added_products : list = [] )-> None:
        """
        1. Assert product count
        2. Assert each product's details: name, image, description, price
        3. If product is added to cart, assert remove button is visible
        """

        expected_count = len(products)

        for i in range(expected_count):
            product_card = self.inventory_items.nth(i)
            product = products[i]

            product_name = product_card.locator(self.ITEM_NAME).inner_text()

            if product_name in added_products:
                expect(product_card.locator(self.REMOVE_BUTTON_FIELD)).to_be_visible()

            # assert product details
            expect(product_card.locator(self.ITEM_IMG)).to_have_attribute("src", product.image_path)
            expect(product_card.locator(self.ITEM_NAME)).to_have_text(product.name)
            expect(product_card.locator(self.ITEM_DESC)).to_contain_text(product.description)
            expect(product_card.locator(self.ITEM_PRICE)).to_have_text(f"${product.price:.2f}")
