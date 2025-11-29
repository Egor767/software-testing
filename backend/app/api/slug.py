from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from backend.app.core.dependencies import get_slug_maker
from backend.app.core.schemas import SlugRead, SlugCreate, SlugBase

if TYPE_CHECKING:
    from backend.app.core.slug import SlugMaker

router = APIRouter(
    prefix="/api",
    tags=["Slug"],
)


@router.post(
    "/link",
    name="slug:create_slug",
    response_model=SlugRead,
)
async def make_slug_from_url(
    slug_data: SlugCreate,
    slug_maker: Annotated[
        "SlugMaker",
        Depends(get_slug_maker),
    ],
) -> SlugRead:
    return await slug_maker.make_slug(slug_data)


@router.get("/s/{short_code}")
async def get_slug(
    short_code: str,
    slug_maker: Annotated[
        "SlugMaker",
        Depends(get_slug_maker),
    ],
):
    long_url = await slug_maker.get_slug_by_code(short_code)
    return RedirectResponse(url=long_url)
