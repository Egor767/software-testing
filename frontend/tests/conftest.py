import pytest
from faker import Faker
from pathlib import Path
from pact import Pact
from playwright.sync_api import Page

SLUG_LEN = 10


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def random_long_url(faker):
    return faker.url()


@pytest.fixture
def slug_len():
    return SLUG_LEN


@pytest.fixture
def api_url():
    return "http://localhost:8080"


@pytest.fixture
def streamlit_url():
    return "http://localhost:8501"


@pytest.fixture(scope="function")
def setup_page(page: Page):
    page.set_viewport_size({"width": 1280, "height": 720})
    yield page


@pytest.fixture(scope="session")
def pact():
    pacts_dir = Path(__file__).parent.parent.parent / "pacts"
    pacts_dir.mkdir(exist_ok=True)

    pact = Pact(consumer="frontend", provider="backend")
    yield pact
    pact.write_file(str(pacts_dir))
