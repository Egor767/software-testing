import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from faker import Faker
from pydantic import HttpUrl

from backend.main import app
from backend.app.api.slug import get_slug_maker
from backend.app.core.schemas import SlugRead
from backend.app.core.slug_size import slug_size
from backend.app.core.schemas import SlugCreate


@pytest.fixture(scope="session")
def fake():
    return Faker()


@pytest.fixture()
def api_url():
    return "http://localhost:8080"


@pytest.fixture
def mock_database():
    with patch("backend.main.db_helper") as mock_db:
        mock_async_conn = AsyncMock()
        mock_db.engine.begin.return_value.__aenter__.return_value = mock_async_conn
        mock_db.engine.begin.return_value.__aexit__.return_value = None

        yield mock_db


@pytest.fixture
def client(mock_database):
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_slug_maker():
    return AsyncMock()


@pytest.fixture
def slug_create_data(fake):
    url = HttpUrl(fake.url())
    return SlugCreate(long_url=url)


@pytest.fixture
def short_code(fake):
    return fake.pystr(min_chars=slug_size, max_chars=slug_size)


@pytest.fixture
def slug_read_data(fake, api_url, short_code):
    return SlugRead(slug=f"{api_url}/api/s/{short_code}")


@pytest.fixture
def slug_test_data(fake, short_code):
    url = HttpUrl(fake.url())
    return {
        "long_url": str(url),
        "slug_code": short_code,
    }


@pytest.fixture
def override_dependencies(mock_slug_maker):
    def _override(dependency=None, mock_obj=None):
        if dependency is None:
            dependency = get_slug_maker
        if mock_obj is None:
            mock_obj = mock_slug_maker

        app.dependency_overrides[dependency] = lambda: mock_obj
        return mock_obj

    return _override


@pytest.fixture(autouse=True)
def auto_clear_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()
