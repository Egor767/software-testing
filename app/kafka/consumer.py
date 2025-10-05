import json
from aiokafka import AIOKafkaConsumer
import logging

logger = logging.getLogger("kafka-consumer")


class KafkaConsumer:
    def __init__(self,
                 bootstrap_servers: str,
                 topics: list,
                 group_id: str,
                 auto_offset_reset: str = "earliest"):
        self.bootstrap_servers = bootstrap_servers
        self.topics = list(topics)
        self.group_id = group_id

        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

    async def start(self):
        await self.consumer.start()
        try:
            sub = self.consumer.subscription()
        except Exception:
            sub = None
        logger.info("Kafka consumer started (bootstrap=%s, group=%s) subscription=%s",
                    self.bootstrap_servers, self.group_id, sub
        )

    async def stop(self):
        await self.consumer.stop()
        logger.info("Kafka consumer stopped (bootstrap=%s, group=%s)",
                    self.bootstrap_servers, self.group_id
        )

    async def get_messages(self):
        async for message in self.consumer:
            yield message.value
