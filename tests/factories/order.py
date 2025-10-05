import factory
import uuid
from factory.alchemy import SQLAlchemyModelFactory
from app.models.order import OrderModel


class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrderModel
        sqlalchemy_session = None

    oid = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=100)

