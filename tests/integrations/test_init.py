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
                             notification_service
                             ):
    # order_service part
    orders_in_db = []
    orders_in_factory = order_factory.build_batch(5)

    for factory_order in orders_in_factory:
        created_order = await order_service.create_order(
            oid=factory_order.oid,
            name=factory_order.name,
            quantity=factory_order.quantity
        )
        orders_in_db.append(created_order)

    for created_order, factory_order in zip(orders_in_db, orders_in_factory):
        assert created_order.oid == factory_order.oid
        assert created_order.name == factory_order.name
        assert created_order.quantity == factory_order.quantity

    # send
    for order in orders_in_db:
        await order_service.send_event(order)

    received_messages = []
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < 10:
        try:
            message = await asyncio.wait_for(notification_service.consumer.consumer.getone(), timeout=1.0)
            received_messages.append(message.value)
            logger.info(f"Received message: {message.value}")
        except asyncio.TimeoutError:
            continue

    assert len(received_messages) == len(orders_in_db)

    for created_order, received_message in zip(orders_in_db, received_messages):
        assert str(created_order.oid) == received_message.get('oid')
        assert created_order.name == received_message.get('name')
        assert created_order.quantity == received_message.get('quantity')

