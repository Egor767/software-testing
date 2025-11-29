from pact import Pact, match
import pytest
import requests

SLUG_LEN = 10


@pytest.fixture
def pact():
    pact = Pact(consumer="frontend", provider="url-shortener")
    yield pact
    pact.write_file("./pacts")


def test_create_short_url(pact):
    example_url = f"http://localhost:8000/s/example-some-site.com"

    (
        pact.upon_receiving("request to create short link")
        .given("backend accepts link creation")
        .with_request("POST", "/api/link")
        .with_body({"long_url": example_url})
        .will_respond_with(200)
        .with_body(
            {
                "slug": match.regex(
                    "http://localhost:8000/s/abcdefghij",
                    regex=rf"^http://localhost:8000/s/.{SLUG_LEN}$",
                ),
            }
        )
    )

    with pact.serve() as server:
        resp = requests.post(f"{server.url}/api/link", json={"long_url": example_url})
        assert resp.status_code == 200
        j = resp.json()
        assert "slug" in j
