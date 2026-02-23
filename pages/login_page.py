from playwright.sync_api import Locator, Page, expect
import re
import pytest

class LoginPage :

    #-----------selectors----------------
    USERNAME_FIELD = 'input[name="user-name"]'
    PASSWORD_FIELD = 'input[name="password"]'
    SUBMIT_BUTTON = 'input[name="login-button"]'

    #---------------page texts------------------
    LOGIN_HEADING = re.compile(r"Swag Labs", re.I)
    ERROR_MESSAGE_FIELD = '[data-test="error"]'
    LOGIN_ERROR_MESSAGE = re.compile("Sorry, this user has been locked out", re.I)

    #---------------Validations-----------
    INVENTORY_URL = re.compile(r"inventory.html", re.I)

    def __init__(self, page: Page) -> None:
        self.page = page


    #--------------locators---------------
    @property
    def username(self) -> Locator:
        return self.page.locator(self.USERNAME_FIELD)
    
    @property
    def password(self) -> Locator:
        return self.page.locator(self.PASSWORD_FIELD)
    
    @property
    def submit(self) -> Locator:
        return self.page.locator(self.SUBMIT_BUTTON)
    
    @property
    def login_heading(self) -> Locator:
        return self.page.get_by_text(self.LOGIN_HEADING)
    
    @property
    def error_message(self) -> Locator:
        return self.page.locator(self.ERROR_MESSAGE_FIELD)

    #-------------navigations--------------
    def open_page(self, url) -> None:
        self.page.goto(url)

    def open_page_and_wait_until_page_is_ready(self, url) -> None:
        self.open_page(url)
        self.wait_until_page_fields_are_ready()

    #-------------assertions--------------
    def wait_until_page_fields_are_ready(self) -> None:
        fields = (self.username, self.password, self.login_heading)

        for field in fields:
            expect(field).to_be_visible()
    
    def wait_for_login_error(self) -> None:
        expect(self.error_message).to_have_text(self.LOGIN_ERROR_MESSAGE)
    #--------------actions---------------
    def enter_username(self, username) -> None:
        self.username.fill(username)
    
    def enter_password(self, password) -> None:
        self.password.fill(password)
    
    def press_login(self) -> None:
        self.submit.click()

    def login(self, username, password = "secret_sauce") -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.press_login()
        self.wait_for_successful_login()

    
    #-------------Post actions--------------
    def wait_for_successful_login(self) -> None:
        expect(self.page).to_have_url(self.INVENTORY_URL)

    
    #-------------E2E Flows--------------
    def open_and_login(self, url: str, username: str, password: str = "secret_sauce") -> None:
        """
        1. Navigate to the login page URL.
        2. Wait until the login page fields are visible and enabled.
        3. Enter the provided username/email.
        4. Enter the provided password.
        5. Submit the login form.
        6. Wait until a successful login indicator is visible.
        """
        self.open_page_and_wait_until_page_is_ready(url)
        self.login(username, password)

        if username != "locked_out_user" :
            self.wait_for_successful_login()


