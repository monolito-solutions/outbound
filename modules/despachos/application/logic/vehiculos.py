from dataclasses import asdict
import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

class ProductPayload(Record):
    product_id = String()
    supplier_id = String()
    name = String()
    description = String()
    price = Float()
    quantity = Long()

    def dict(self):
        return str({k: str(v) for k, v in asdict(self).items()})
    
def get_vehicle(total_quantity):
    if total_quantity > 8:
        return "veh_3"
    elif total_quantity > 5:
        return "veh_2"
    else:
        return "veh_1"
    
def vehiculos_minimo(order_items_str):
    # Parsear el string de order_items en una lista de objetos ProductPayload
    try:  
        order_items = [ProductPayload.from_json(item_str) for item_str in eval(order_items_str)]
    
        # Sumar las cantidades de todos los objetos ProductPayload en la lista
        total_quantity = sum([item.quantity for item in order_items])
        vehicle = get_vehicle(total_quantity)
        return vehicle
    except Exception as e:
        print(f"Error creating order: {e}")
        return get_vehicle(3)
    