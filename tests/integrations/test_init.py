import asyncio
import json

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
    # order_service part (не меняем)
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

    # СНАЧАЛА ОТПРАВЛЯЕМ СООБЩЕНИЯ
    for order in orders_in_db:
        await order_service.send_event(order)

    # R.I.P.
