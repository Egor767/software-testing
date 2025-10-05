# tests/conftest.py
import os
import pytest
from testcontainers.postgres import PostgresContainer
from app.db.session import init_engine, create_tables, drop_tables, get_db_session
from app.kafka.producer import KafkaProducer
from app.services.order import OrderService
from tests.integrations.utils import run_sync


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with PostgresContainer("postgres:16-alpine") as postgres:
        os.environ["DB_HOST"] = postgres.get_container_host_ip()
        os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
        os.environ["DB_USERNAME"] = postgres.username
        os.environ["DB_PASSWORD"] = postgres.password
        os.environ["DB_NAME"] = postgres.dbname

        init_engine()
        run_sync(create_tables())
        yield
        # run_sync(drop_tables())


@pytest.fixture(scope="function")
def db_session():
    async def _get():
        async for s in get_db_session():
            return s
    return run_sync(_get())


class DummyProducer:
    async def send(self, topic, message):
        return f"sent_to_{topic}"


@pytest.fixture(scope="function")
def order_service(db_session):
    return OrderService(db_session, KafkaProducer(), "order_topic")

