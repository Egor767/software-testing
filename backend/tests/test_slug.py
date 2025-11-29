import pytest
from fastapi import HTTPException
from backend.app.core.schemas import SlugRead
from backend.app.core.slug_size import slug_size


@pytest.mark.asyncio
async def test_make_slug(
    client,
    slug_create_data,
    mock_slug_maker,
    override_dependencies,
    fake,
):
    slug_code = fake.pystr(min_chars=slug_size, max_chars=slug_size)

    full_url = f"http://localhost:8080/api/s/{slug_code}"
    expected_slug_read = SlugRead(slug=full_url)

    mock_slug_maker.make_slug.return_value = expected_slug_read
    override_dependencies()

    response = client.post("/api/link", json=slug_create_data.model_dump())

    assert response.status_code == 200

    data = response.json()
    assert "slug" in data

    assert data["slug"] == full_url
    assert data["slug"].startswith("http://localhost:8080/api/s/")
    assert data["slug"].endswith(slug_code)


@pytest.mark.asyncio
async def test_get_slug_redirect(
    client,
    mock_slug_maker,
    override_dependencies,
    fake,
):
    slug_code = fake.pystr(min_chars=slug_size, max_chars=slug_size)
    long_url = fake.url()

    mock_slug_maker.get_slug_by_code.return_value = long_url
    override_dependencies()

    response = client.get(f"/api/s/{slug_code}", follow_redirects=False)

    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"] == long_url

    mock_slug_maker.get_slug_by_code.assert_called_once_with(slug_code)


@pytest.mark.asyncio
async def test_get_slug_not_found(
    client,
    mock_slug_maker,
    override_dependencies,
    fake,
):
    slug_code = fake.pystr(min_chars=slug_size, max_chars=slug_size)

    mock_slug_maker.get_slug_by_code.side_effect = HTTPException(
        status_code=404, detail="Slug not found"
    )
    override_dependencies()

    response = client.get(f"/api/s/{slug_code}")

    assert response.status_code == 404
    assert "Slug not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_make_slug_already_exists(
    client,
    slug_create_data,
    mock_slug_maker,
    override_dependencies,
):
    mock_slug_maker.make_slug.side_effect = HTTPException(
        status_code=400, detail="Already Exist"
    )
    override_dependencies()

    response = client.post("/api/link", json=slug_create_data.model_dump())

    assert response.status_code == 400
    assert "Already Exist" in response.json()["detail"]
