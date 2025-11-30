import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.api import api_router
from backend.app.core.models import Base, db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Short URL Maker",
    version="1.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/hello")
async def hello():
    return "Hello!"

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        f"{__name__}:app",
        host="localhost",
        port=8080,
        reload=True,
        log_level="info",
    )
