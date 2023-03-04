import utils
from fastapi import FastAPI
from infrastructure.dispatchers import Dispatcher
import uvicorn
import asyncio
from sqlalchemy.exc import OperationalError
from infrastructure.consumers import subscribe_to_topic
from modules.despachos.application.events.events import  OrderDispatchedPayload, EventOrderDispatched
from modules.despachos.application.commands.commands import CheckOrderPayload, CommandCheckOrder
from api.errors.exceptions import BaseAPIException
from api.errors.handlers import api_exeption_handler
from config.db import Base, engine, initialize_base

app = FastAPI()
app.add_exception_handler(BaseAPIException, api_exeption_handler)


tasks = list()
initialize_base()
try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(subscribe_to_topic(
        "order-events", "sub-orders", EventOrderDispatched))
    task2 = asyncio.ensure_future(subscribe_to_topic(
        "order-commands", "sub-com-order-checkinventory", CommandCheckOrder))
    tasks.append(task1)
    tasks.append(task2)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/health", status_code=202)
def health():
    event_payload = OrderDispatchedPayload(
        order_id = str("order id 1"),
        customer_id = str("costumer id 1"),
        order_date = str("order date"),
        order_status = str("order status"),
        order_items = str("order other"),
        order_total = float(2),
        order_version = int(1)
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
    dispatcher.publish_message(command, "order-commands")
    return {"status":"ok"}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=6969)