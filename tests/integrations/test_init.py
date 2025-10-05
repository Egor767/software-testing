import asyncio

import pytest
from sqlalchemy import text
import logging

logger = logging.getLogger("test-logger")


@pytest.mark.asyncio
async def test_table_exist(db_session, setup_database):
    table_name = "order"
    query = text(
        "SELECT EXISTS ("
        "SELECT FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = :table_name)"
    )
    result = await db_session.execute(query, {"table_name": table_name})
    exists = result.scalar()

    assert exists


@pytest.mark.asyncio
async def test_full_scenario(caplog,
                             db_session,
                             order_service,
                             order_factory,
                             consumer):
    orders_in_db = []
    orders_in_factory = order_factory.build_batch(5)
    for factory_order in orders_in_factory:
        created_order = await order_service.create_order(
            oid=factory_order.oid,
            name=factory_order.name,
            quantity=factory_order.quantity
        )
        orders_in_db.append(created_order)
        await order_service.send_event(created_order)

    received_messages = []
    start_time = asyncio.get_event_loop().time()

    while len(received_messages) < len(orders_in_db) and (asyncio.get_event_loop().time() - start_time) < 10:
        try:
            message = await asyncio.wait_for(consumer.consumer.getone(), timeout=1.0)
            received_messages.append(message.value)
            logger.info(f"Received message: {message.value}")
        except asyncio.TimeoutError:
            continue

    assert len(received_messages) == len(orders_in_db)
