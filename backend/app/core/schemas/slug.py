from pydantic import BaseModel, HttpUrl


class SlugBase(BaseModel):
    long_url: HttpUrl


class SlugCreate(SlugBase):
    pass


class SlugRead(BaseModel):
    slug: str
