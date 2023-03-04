
from config.db import get_db
from fastapi import Depends
from modules.despachos.application.events.events import OrderDispatchedPayload, ProductPayload, EventOrderDispatched
from modules.despachos.infrastructure.repositories import DespachosRepositorySQLAlchemy
from modules.despachos.application.commands.commands import CommandCheckOrder, CheckOrderPayload
from sqlalchemy.exc import IntegrityError
from api.errors.exceptions import BaseAPIException
from infrastructure.dispatchers import Dispatcher
import utils
from modules.despachos.domain.entities import Despacho

def iniciar_despacho(order, db=Depends(get_db)):
    try:
        params = dict(
            order_id = order.order_id,
            customer_id = order.customer_id,
            order_date = order.order_date,
            order_status = order.order_status,
            order_items = order.order_items,
            order_total = order.order_total,
            pod_id = "pod_1",
            date_despacho = "2023-02-27T08:06:08.464634",
            vehiculo_minimo_code = "veh_1",
            order_version = order.order_version
        )
        print ("en llamado de iniciar despacho")
        print (params)
        despacho = Despacho(**params)
        repository = DespachosRepositorySQLAlchemy(db)
        repository.create(despacho)
    except IntegrityError:
        raise BaseAPIException(f"Error creating order, primary key integrity violated (Duplicate ID)", 400)
    except Exception as e:
        raise BaseAPIException(f"Error creating order: {e}", 500)


    return {"message": "Order created successfully"}

def desde_logic():
    print ("")