import logging
import json

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
            payload = event
            oid = payload.get("oid")
            name = payload.get("name")
            quantity = payload.get("quantity")
            logger.info(f"Received new order event: oid={oid}, name={name}, quantity={quantity}")

    async def old_run(self):
        try:
            bootstrap = getattr(self.consumer, "bootstrap_servers", None)
            topics = getattr(self.consumer, "topics", None)
            group = getattr(self.consumer, "group_id", None)
            logger.info("NotificationService.run: consumer bootstrap=%s topics=%s group=%s",
                        bootstrap, topics, group)
        except Exception:
            logger.exception("Failed to introspect consumer attributes")

        async for event in self.consumer.get_messages():
            if event is None:
                logger.warning("Received None event")
                continue
            logger.debug("Raw received event: %r", event)

            payload = event
            if not isinstance(payload, dict):
                try:
                    if isinstance(payload, (bytes, bytearray)):
                        payload = json.loads(payload.decode("utf-8"))
                    elif isinstance(payload, str):
                        payload = json.loads(payload)
                    else:
                        payload = {}
                except Exception:
                    logger.exception("Failed to decode payload: %r", payload)
                    payload = {}

            oid = payload.get("oid")
            name = payload.get("name")
            quantity = payload.get("quantity")

            logger.info(f"Received new order event: oid={oid}, name={name}, quantity={quantity}")

