"""
conftest.py = shared setup code that pytest loads automatically.

Anything defined here with @pytest.fixture can be used by ANY test file
just by adding its name as a function argument. That is called "dependency
injection" and it's the most important idea in pytest.
"""
import pytest
import requests

# JSONPlaceholder is a free fake REST API made for practice and testing.
API_BASE_URL = "https://jsonplaceholder.typicode.com"

# Sauce Demo is a free demo shopping website made for practicing UI automation.
UI_BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(scope="session")
def api_url():
    """The base URL of the API. 'session' scope = created once per test run."""
    return API_BASE_URL


@pytest.fixture(scope="session")
def api_client():
    """
    A reusable HTTP session. Re-using one session is faster than opening a
    brand-new connection for every request.
    """
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session  # everything before 'yield' is setup
    session.close()  # everything after 'yield' is cleanup (teardown)


@pytest.fixture(scope="session")
def ui_url():
    """The base URL of the website under test."""
    return UI_BASE_URL
