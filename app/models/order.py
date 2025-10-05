import uuid
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OrderModel(Base):
    __tablename__ = 'order'

    oid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer)

