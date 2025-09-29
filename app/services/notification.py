import logging
logger = logging.getLogger("notification-service")


class NotificationService:
    def __init__(self, consumer):
        self.consumer = consumer

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def run(self):
        async for event in self.consumer.get_messages():
            oid = event.get("oid")
            name = event.get("name")
            quantity = event.get("quantity")
            logger.info(f"Received new order event: oid={oid}, name={name}, quantity={quantity}")

