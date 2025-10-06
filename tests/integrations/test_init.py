import asyncio
import pytest
from sqlalchemy import text, select
import logging

from app.models.order import OrderModel

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
    # order_service (create orders)
    orders_in_factory = order_factory.build_batch(5)

    for factory_order in orders_in_factory:
        await order_service.create_order(
            oid=factory_order.oid,
            name=factory_order.name,
            quantity=factory_order.quantity
        )

    # check orders in db
    stmt = select(OrderModel)
    result = await db_session.execute(stmt)
    orders_in_db = result.scalars().all()

    assert len(orders_in_db) == len(orders_in_db)
    for created_order, db_order in zip(orders_in_db, orders_in_db):
        assert created_order.oid == db_order.oid
        assert created_order.name == db_order.name
        assert created_order.quantity == db_order.quantity

    # send msgs to consumer
    for order in orders_in_db:
        await order_service.send_event(order)

    # get msgs from consumer
    received_messages = []
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < 10:
        try:
            message = await asyncio.wait_for(notification_service.consumer.consumer.getone(), timeout=1.0)
            received_messages.append(message.value)
            logger.info(f"Received message: {message.value}")
        except asyncio.TimeoutError:
            continue

    # check msgs from consumer
    assert len(received_messages) == len(orders_in_db)
    for created_order, received_message in zip(orders_in_db, received_messages):
        assert str(created_order.oid) == received_message.get('oid')
        assert created_order.name == received_message.get('name')
        assert created_order.quantity == received_message.get('quantity')

