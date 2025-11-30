from pact import Pact, match
import pytest
import requests

def test_create_short_url(pact, slug_len, random_long_url):
    (
        pact
        .upon_receiving("request to create short link")
        .given("backend accepts link creation")
        .with_request("POST", "/api/link")
        .with_header("Content-Type", "application/json")
        .with_body({"long_url": random_long_url})
        .will_respond_with(200)
        .with_body({
            "slug": match.regex(
                "http://localhost:8080/api/s/abcdefghij",
                regex=rf"^http://localhost:8080/api/s/.{{{slug_len}}}$",
            )
        })
    )

    with pact.serve() as server:
        resp = requests.post(
            f"{server.url}/api/link",
            json={"long_url": random_long_url}
        )
        assert resp.status_code == 200
        j = resp.json()
        assert "slug" in j