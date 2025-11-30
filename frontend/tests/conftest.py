import pytest
from faker import Faker
from pathlib import Path
from pact import Pact

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


@pytest.fixture(scope="session")
def pact():
    pacts_dir = Path(__file__).parent.parent.parent / "pacts"
    pacts_dir.mkdir(exist_ok=True)

    pact = Pact(consumer="frontend", provider="backend")
    yield pact
    pact.write_file(str(pacts_dir))
