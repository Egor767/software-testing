from fastapi import APIRouter

from .slug import router as slug_router

api_router = APIRouter()

api_router.include_router(slug_router)
