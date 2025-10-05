import os

import pytest_asyncio
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError, GroupCoordinatorNotAvailableError
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from app.db.session import init_engine, create_tables, drop_tables, get_db_session
from app.kafka.consumer import KafkaConsumer
from app.kafka.producer import KafkaProducer
from app.services.notification import NotificationService
from app.services.order import OrderService
from tests.factories.order import OrderFactory
from pytest_factoryboy import register
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
import asyncio

register(OrderFactory)


# Containers
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    with PostgresContainer("postgres:16-alpine") as postgres:
        os.environ["DB_HOST"] = postgres.get_container_host_ip()
        os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
        os.environ["DB_USERNAME"] = postgres.username
        os.environ["DB_PASSWORD"] = postgres.password
        os.environ["DB_NAME"] = postgres.dbname

        init_engine()
        await create_tables()
        yield
        await drop_tables()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_kafka_container():
    with KafkaContainer().with_kraft() as kafka:
        bootstrap_server = kafka.get_bootstrap_server()
        os.environ["KAFKA_BOOTSTRAP_SERVERS"] = bootstrap_server

        admin = AIOKafkaAdminClient(bootstrap_servers=bootstrap_server)
        await admin.start()
        topics = await admin.list_topics()
        topic: str = "test_topic"
        if topic not in topics:
            await admin.create_topics([
                NewTopic(name=topic, num_partitions=1, replication_factor=1)
            ])
        await admin.close()

        yield


# functions
@pytest_asyncio.fixture(scope="function")
async def db_session():
    async for session in get_db_session():
        yield session


@pytest_asyncio.fixture(scope="function")
async def producer():
    producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture(scope="function")
async def order_service(db_session, producer):
    order_service = OrderService(db_session, producer, "test_topic")
    yield order_service


@pytest_asyncio.fixture(scope="function")
async def consumer():
    consumer = KafkaConsumer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        topics=['test_topic'],
        group_id="test_group"
    )
    await consumer.start()
    yield consumer
    await consumer.stop()


@pytest_asyncio.fixture(scope="function")
async def notification_service(consumer):
    notification_service = NotificationService(consumer)
    yield notification_service

