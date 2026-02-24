import re
import pytest
from playwright.sync_api import Locator, expect
from pages.login_page import LoginPage

@pytest.mark.negative
def test_login_not_work(login_as_locked_out_user):
    page = login_as_locked_out_user
    login_page = LoginPage(page)

    login_page.wait_for_login_error()


