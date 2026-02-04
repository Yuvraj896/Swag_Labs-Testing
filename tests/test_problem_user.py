import re
import pytest
from playwright.sync_api import Locator, Page, expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_problem_user_buying_functionalities(login_as_problem_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.problem_user_cart_behaviour()

def test_problem_user_navigation_func(login_as_problem_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.standard_user_cart_page_navigation_and_state()

def test_problem_user_broken_image(login_as_problem_user, page):
    dashboard_page = DashboardPage(page)
    dashboard_page.problem_user_verify_broken_image()
    
