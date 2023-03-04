
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
    print ("otro")

def desde_logic():
    print (" soy logic")