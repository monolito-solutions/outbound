from dataclasses import dataclass
from typing import List
import uuid
from datetime import datetime


@dataclass(frozen=True)
class Despacho:
    order_id: uuid.uuid4()
    customer_id: uuid.uuid4()
    order_date: str
    order_status: str
    order_items: List[dict]
    order_total: float
    pod_id: str
    date_despacho: str
    vehiculo_minimo_code: str
    order_version: int = 2


    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_items": self.order_items,
            "order_total": self.order_total,
            "pod_id": self.pod_id,
            "date_despacho": self.date_despacho,
            "vehiculo_minimo_code": self.vehiculo_minimo_code,
            "order_version": self.order_version,
        }