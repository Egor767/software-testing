import json
from aiokafka import AIOKafkaConsumer
import logging

logger = logging.getLogger("kafka-consumer")


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, topics: list, group_id: str):
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        )

    async def start(self):
        await self.consumer.start()
        logger.info(f"Kafka consumer started for topics {self.consumer.subscription()}")

    async def stop(self):
        await self.consumer.stop()
        logger.info("Kafka consumer stopped")

    async def get_messages(self):
        async for message in self.consumer:
            yield message.value

