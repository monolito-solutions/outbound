
from config.db import get_db
from fastapi import Depends
from modules.despachos.application.events.events import OrderDispatchedPayload, ProductPayload, EventOrderDispatched
from modules.despachos.infrastructure.repositories import DespachosRepositorySQLAlchemy
from modules.despachos.application.commands.commands import CommandCheckOrder, CheckOrderPayload
from sqlalchemy.exc import IntegrityError
from api.errors.exceptions import BaseAPIException
from infrastructure.dispatchers import Dispatcher
import utils

def iniciar_despacho(order, db=Depends(get_db)):
    try:
        repository = DespachosRepositorySQLAlchemy(db)
        repository.create(order)
    except IntegrityError:
        raise BaseAPIException(f"Error creating order, primary key integrity violated (Duplicate ID)", 400)
    except Exception as e:
        raise BaseAPIException(f"Error creating order: {e}", 500)

    event_payload = OrderDispatchedPayload(
        order_id = str(order.order_id),
        customer_id = str(order.customer_id),
        order_date = str(order.order_date),
        order_status = str(order.order_status),
        order_items = str([str(ProductPayload(**item))for item in order.order_items]),
        order_total = float(order.order_total),
        order_version = int(order.order_version)
    )

    event = EventOrderDispatched(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = OrderDispatchedPayload.__name__,
        data_payload = event_payload
    )

    command_payload = CheckOrderPayload(**event_payload.to_dict())
    command_payload.order_status = "Ready to check inventory"

    command = CommandCheckOrder(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = CheckOrderPayload.__name__,
        data_payload = command_payload
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "order-events")
    dispatcher.publish_message(command, "order-commands")


    return {"message": "Order created successfully"}

def desde_logic():
    print (" soy logic")