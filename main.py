from fastapi import FastAPI
import uvicorn
import asyncio
from sqlalchemy.exc import OperationalError
from infrastructure.consumers import subscribe_to_topic
from modules.orders.application.events.events import EventOrderCreated
from modules.orders.application.commands.commands import CommandCheckInventoryOrder
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
        "order-events", "sub-orders", EventOrderCreated))
    task2 = asyncio.ensure_future(subscribe_to_topic(
        "order-commands", "sub-com-order-checkinventory", CommandCheckInventoryOrder))
    tasks.append(task1)
    tasks.append(task2)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/health", status_code=202)
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=6969)