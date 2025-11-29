from typing import AsyncGenerator, Annotated, TYPE_CHECKING

from fastapi import Depends

from backend.app.core.models import db_helper
from backend.app.core.slug import SlugMaker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[
    "AsyncSession",
    None,
]:
    async for session in db_helper.session_dependency():
        yield session


async def get_slug_maker(
    session: Annotated[
        "AsyncSession",
        Depends(get_db_session),
    ],
) -> SlugMaker:
    yield SlugMaker(session)
