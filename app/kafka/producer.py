from aiokafka import AIOKafkaProducer
import logging

logger = logging.getLogger("kafka-producer")


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()
        logger.info("Kafka producer started (bootstrap=%s)", self.bootstrap_servers)

    async def stop(self):
        await self.producer.stop()
        logger.info("Kafka producer stopped (bootstrap=%s)", self.bootstrap_servers)

    async def send(self, topic: str, message: bytes):
        result = await self.producer.send_and_wait(topic, message)
        logger.debug("Producer.send: topic=%s result=%s", topic, result)
        return result

