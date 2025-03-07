import asyncio

from fastapi import FastAPI
import uvicorn

from trainings_app.db.connection import AsyncpgPool
from trainings_app.routers import users, clients, memberships, trainings, exercises, trainings_exercises, root
from trainings_app.auth.routers import jwt_auth
from trainings_app.exceptions.exception_handlers import (
    record_not_found_handler,
    convert_record_handler,
    access_denied_handler,
)
from trainings_app.exceptions.exceptions import RecordNotFoundError, ConvertRecordError
from trainings_app.tg_bot.bot import start_bot

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Initialize the application server."""

    await AsyncpgPool.setup()
    asyncio.create_task(start_bot())


@app.on_event("shutdown")
async def shutdown():
    """Close connection pool in case of application shutdown."""

    await AsyncpgPool.close_pool()


app.include_router(router=root.router)
app.include_router(router=users.router)
app.include_router(router=clients.router)
app.include_router(router=memberships.router)
app.include_router(router=trainings.router)
app.include_router(router=exercises.router)
app.include_router(router=trainings_exercises.router)

app.include_router(router=jwt_auth.router)

app.add_exception_handler(RecordNotFoundError, record_not_found_handler)
app.add_exception_handler(ConvertRecordError, convert_record_handler)
app.add_exception_handler(ConvertRecordError, access_denied_handler)

if __name__ == "__main__":
    uvicorn.run("trainings_app.main:app")
