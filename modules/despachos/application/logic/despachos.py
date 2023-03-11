
from config.db import get_db
from fastapi import Depends
from modules.despachos.application.events.events import EventOrderCanceledByPrice, OrderDispatchedPayload, ProductPayload, EventOrderDispatched
from modules.despachos.infrastructure.repositories import DespachosRepositorySQLAlchemy
from modules.despachos.application.commands.commands import CommandCheckOrder, CheckOrderPayload
from sqlalchemy.exc import IntegrityError
from api.errors.exceptions import BaseAPIException
from infrastructure.dispatchers import Dispatcher
import utils
from modules.despachos.domain.entities import Despacho
from modules.despachos.application.logic.prioridad import prioridad
from modules.despachos.application.logic.vehiculos import vehiculos_minimo


def iniciar_despacho(order):
    try:
        db = get_db()
        params = dict(
            order_id = order.order_id,
            customer_id = order.customer_id,
            order_date = order.order_date,
            order_status = order.order_status,
            order_items = order.order_items,
            order_total = order.order_total,
            pod_id = prioridad(valor=order.order_total),
            date_despacho = "2023-02-27T08:06:08.464634",
            vehiculo_minimo_code = vehiculos_minimo(order_items_str=order.order_items),
            order_version = order.order_version
        )
        state_order = "dispatched"
        if ( params.pod_id == "prioridad_critica"):
            state_order = "canceled"
        print ("en llamado de iniciar despacho")
        params.order_status = state_order
        print (params)
        despacho = Despacho(**params)
        repository = DespachosRepositorySQLAlchemy(db)
        repository.create(despacho)
        db.close()
    except IntegrityError:
        raise BaseAPIException(f"Error creating order, primary key integrity violated (Duplicate ID)", 400)
    except Exception as e:
        raise BaseAPIException(f"Error creating order: {e}", 500)

    


    event_payload = OrderDispatchedPayload(
        order_id = str(order.order_id),
        customer_id = str(order.customer_id),
        order_date = str(order.order_date),
        order_status = params.order_status,
        order_items = order.order_items,
        order_total = float(order.order_total),
        order_version = int(order.order_version)
    )
    
    message = "Order created successfully"
    if ( params.order_status == "canceled"):
        event = EventOrderCanceledByPrice(
            time = utils.time_millis(),
            ingestion = utils.time_millis(),
            datacontenttype = OrderDispatchedPayload.__name__,
            data_payload = event_payload
        )
        message = "Order canceled"
    else:     
        event = EventOrderDispatched(
            time = utils.time_millis(),
            ingestion = utils.time_millis(),
            datacontenttype = OrderDispatchedPayload.__name__,
            data_payload = event_payload
        )


    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "order-events")
    
    return {"message": message}

def pod_disponible():
    print ("")


