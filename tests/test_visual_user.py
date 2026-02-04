import re
import pytest
from playwright.sync_api import Locator, Page, expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_visual_user_buying_functionalities(login_as_visual_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.standard_user_shopping_elements()

def test_visual_user_broken_image(login_as_visual_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.problem_user_verify_broken_image()

def test_visual_user_navigation_func(login_as_visual_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.standard_user_cart_page_navigation_and_state()  

def test_visual_user_screenshot(login_as_visual_user, page, assert_snapshot):
    dashboard_page = DashboardPage(page)
    dashboard_page.wait_until_page_fields_are_ready()
    assert_snapshot(page.screenshot(mask=[dashboard_page.price_bar_mask]))