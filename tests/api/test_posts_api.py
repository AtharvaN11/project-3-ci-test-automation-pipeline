"""
API tests: we talk to the REST API directly with HTTP requests (no browser).

HTTP basics you'll see here:
  GET    = read data              -> expect 200 (OK)
  POST   = create data            -> expect 201 (Created)
  DELETE = remove data            -> expect 200 (OK)
  404    = "that thing doesn't exist"

Run only these tests:   pytest -m api
"""
import pytest

# Mark every test in this file as an "api" test (see markers in pytest.ini)
pytestmark = pytest.mark.api

TIMEOUT = 10  # seconds. Always set a timeout so a hung server can't freeze CI.


@pytest.mark.smoke
def test_get_single_post_returns_200(api_client, api_url):
    response = api_client.get(f"{api_url}/posts/1", timeout=TIMEOUT)

    assert response.status_code == 200


def test_get_single_post_has_expected_fields(api_client, api_url):
    response = api_client.get(f"{api_url}/posts/1", timeout=TIMEOUT)
    body = response.json()  # turn the JSON response into a Python dict

    assert body["id"] == 1
    # A good test checks the *shape* of the data, not just the status code.
    for field in ("userId", "id", "title", "body"):
        assert field in body


def test_get_all_posts_returns_100_items(api_client, api_url):
    response = api_client.get(f"{api_url}/posts", timeout=TIMEOUT)

    assert response.status_code == 200
    assert len(response.json()) == 100


def test_filter_posts_by_user(api_client, api_url):
    # "?userId=1" is a query parameter: it filters the results.
    response = api_client.get(f"{api_url}/posts", params={"userId": 1}, timeout=TIMEOUT)

    posts = response.json()
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)


@pytest.mark.smoke
def test_create_post_returns_201(api_client, api_url):
    new_post = {"title": "CI/CD practice", "body": "Created by a test", "userId": 1}

    response = api_client.post(f"{api_url}/posts", json=new_post, timeout=TIMEOUT)

    assert response.status_code == 201
    created = response.json()
    assert created["title"] == new_post["title"]
    assert "id" in created  # the server assigns a new id


def test_unknown_post_returns_404(api_client, api_url):
    response = api_client.get(f"{api_url}/posts/99999", timeout=TIMEOUT)

    assert response.status_code == 404


def test_delete_post_returns_200(api_client, api_url):
    response = api_client.delete(f"{api_url}/posts/1", timeout=TIMEOUT)

    assert response.status_code == 200


@pytest.mark.parametrize("post_id", [1, 25, 50, 100])
def test_several_posts_exist(api_client, api_url, post_id):
    """
    parametrize = run the SAME test with different inputs.
    pytest shows this as 4 separate tests in the report.
    """
    response = api_client.get(f"{api_url}/posts/{post_id}", timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["id"] == post_id
