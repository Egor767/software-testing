import hashlib
import logging
from contextlib import asynccontextmanager
from fastapi import HTTPException
from typing import TYPE_CHECKING

from sqlalchemy import insert, select

from backend.app.core.models import Slug
from backend.app.core.schemas import SlugCreate, SlugRead
from backend.app.core.slug_size import slug_size

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("SlugMaker-Logger")


@asynccontextmanager
async def transaction_manager(session: "AsyncSession"):
    try:
        yield
        await session.commit()
    except Exception:
        await session.rollback()
        raise


class SlugMaker:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self.prefix = "http://localhost:8080/api/s/"

    async def make_slug(self, slug_create_data: SlugCreate) -> SlugRead:
        stmt = select(Slug).where(Slug.long_url == slug_create_data.long_url)
        result = await self.session.execute(stmt)
        existing_slug = result.scalar_one_or_none()

        if existing_slug:
            raise HTTPException(
                status_code=400,
                detail="Already Exist",
            )

        generated_slug = await self.generate_slug(slug_create_data.long_url)

        slug_data = slug_create_data.model_dump()
        slug_data["slug"] = generated_slug

        created_slug = await self.save_slug_to_db(slug_data)
        if not created_slug:
            raise ValueError("Creation failed")

        logger.info("RETURNING SLUG = %r", created_slug)

        return await self.make_short_url(created_slug)

    @staticmethod
    async def generate_slug(long_url: str):
        hash_obj = hashlib.sha256(long_url.encode())
        hash_hex = hash_obj.hexdigest()

        return hash_hex[:slug_size]

    async def save_slug_to_db(self, db_data: dict) -> SlugRead | None:
        stmt = insert(Slug).values(**db_data).returning(Slug)
        async with transaction_manager(self.session):
            result = await self.session.execute(stmt)
            db_slug = result.scalar_one_or_none()
        return db_slug

    async def make_short_url(self, slug: SlugRead) -> SlugRead:
        slug.slug = self.prefix + slug.slug
        return slug

    async def get_slug_by_code(self, short_code: str) -> str:
        stmt = select(Slug).where(Slug.slug == short_code)
        result = await self.session.execute(stmt)
        db_slug = result.scalar_one_or_none()
        if not db_slug:
            raise HTTPException(status_code=404, detail="Slug not found")

        logger.info("RETURNING LONG_URL = %r", db_slug.long_url)
        return db_slug.long_url
