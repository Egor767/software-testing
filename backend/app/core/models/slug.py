from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ..slug_size import slug_size


class Slug(Base):
    __tablename__ = "slugs"

    id: Mapped[int] = mapped_column(primary_key=True)

    long_url: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(slug_size),
        unique=True,
        nullable=False,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}), long_url]{self.long_url}, slug={self.slug})"
