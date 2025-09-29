from aiokafka import AIOKafkaProducer
import logging

logger = logging.getLogger("kafka-producer")


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()
        logger.info(f"Kafka producer started")

    async def stop(self):
        await self.producer.stop()
        logger.info("Kafka producer stopped")

    async def send(self, topic: str, message: bytes):
        return await self.producer.send_and_wait(topic, message)

