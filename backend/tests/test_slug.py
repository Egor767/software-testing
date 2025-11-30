import pytest
from fastapi import HTTPException
from backend.app.core.schemas import SlugRead
from backend.app.core.slug_size import slug_size


@pytest.mark.asyncio
async def test_make_slug(
    client,
    api_url,
    slug_create_data,
    mock_slug_maker,
    override_dependencies,
    fake,
    short_code,
):
    full_url = f"{api_url}/api/s/{short_code}"
    expected_slug_read = SlugRead(slug=full_url)

    mock_slug_maker.make_slug.return_value = expected_slug_read
    override_dependencies()

    response_data = {"long_url": str(slug_create_data.long_url)}
    response = client.post("/api/link", json=response_data)

    assert response.status_code == 200

    data = response.json()
    assert "slug" in data

    assert data["slug"] == full_url
    assert data["slug"].startswith(f"{api_url}/api/s/")
    assert data["slug"].endswith(short_code)


@pytest.mark.asyncio
async def test_get_slug_redirect(
    client,
    mock_slug_maker,
    override_dependencies,
    fake,
    short_code,
):
    long_url = fake.url()

    mock_slug_maker.get_slug_by_code.return_value = long_url
    override_dependencies()

    response = client.get(f"/api/s/{short_code}", follow_redirects=False)

    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"] == long_url

    mock_slug_maker.get_slug_by_code.assert_called_once_with(short_code)


@pytest.mark.asyncio
async def test_get_slug_not_found(
    client,
    mock_slug_maker,
    override_dependencies,
    fake,
    short_code,
):
    mock_slug_maker.get_slug_by_code.side_effect = HTTPException(
        status_code=404, detail="Slug not found"
    )
    override_dependencies()

    response = client.get(f"/api/s/{short_code}")

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

    response_data = {"long_url": str(slug_create_data.long_url)}
    response = client.post("/api/link", json=response_data)

    assert response.status_code == 400
    assert "Already Exist" in response.json()["detail"]
