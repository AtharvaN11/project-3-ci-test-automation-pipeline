"""
UI tests: Playwright opens a real (headless) Chromium browser and clicks
through the website like a user would.

"headless" = the browser runs without a visible window (needed in CI).
The `page` argument is a fixture provided by the pytest-playwright plugin.

Run only these tests:   pytest -m ui
"""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.ui

# Public demo credentials published by saucedemo.com for practice.
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"


def login(page: Page, base_url: str, username: str, password: str) -> None:
    """Helper: fill in the login form and press the button."""
    page.goto(base_url)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


@pytest.mark.smoke
def test_valid_login_shows_products(page: Page, ui_url):
    login(page, ui_url, VALID_USER, PASSWORD)

    # expect(...) automatically WAITS (up to a few seconds) for the condition,
    # which makes UI tests much less flaky than a fixed sleep().
    expect(page).to_have_url(f"{ui_url}/inventory.html")
    expect(page.locator(".inventory_item")).to_have_count(6)


def test_wrong_password_shows_error(page: Page, ui_url):
    login(page, ui_url, VALID_USER, "wrong_password")

    error = page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")


def test_locked_out_user_cannot_login(page: Page, ui_url):
    login(page, ui_url, LOCKED_USER, PASSWORD)

    expect(page.locator("[data-test='error']")).to_contain_text("locked out")


def test_empty_username_shows_error(page: Page, ui_url):
    page.goto(ui_url)
    page.click("#login-button")  # submit the empty form

    expect(page.locator("[data-test='error']")).to_contain_text("Username is required")


def test_add_item_to_cart_updates_badge(page: Page, ui_url):
    login(page, ui_url, VALID_USER, PASSWORD)

    page.click("[data-test='add-to-cart-sauce-labs-backpack']")

    # The little number on the cart icon should now say 1.
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_logout_returns_to_login_page(page: Page, ui_url):
    login(page, ui_url, VALID_USER, PASSWORD)

    page.click("#react-burger-menu-btn")  # open the side menu
    page.click("#logout_sidebar_link")

    expect(page).to_have_url(f"{ui_url}/")
    expect(page.locator("#login-button")).to_be_visible()
