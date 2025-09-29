import json
import logging
from app.models.order import OrderModel

logger = logging.getLogger("order-service")


class OrderService:
    def __init__(self, db_session, producer, topic: str):
        self.session = db_session
        self.producer = producer
        self.topic = topic

    async def create_order(self, name: str, quantity: int):
        new_order = OrderModel(name=name, quantity=quantity)
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        logger.info(f"Created new order: oid={new_order.oid}, name={new_order.name}, quantity={new_order.quantity}")

        return new_order

    async def send_event(self, new_order: OrderModel):
        event = {
            "oid": str(new_order.oid),
            "item_name": new_order.name,
            "quantity": new_order.quantity
        }
        result = await self.producer.send(self.topic, json.dumps(event).encode("utf-8"))
        logger.info(f"Send order to producer: {result}")

        return result

