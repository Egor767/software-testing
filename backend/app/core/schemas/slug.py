from pydantic import BaseModel


class SlugBase(BaseModel):
    long_url: str


class SlugCreate(SlugBase):
    pass


class SlugRead(BaseModel):
    slug: str
