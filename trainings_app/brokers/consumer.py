import asyncio
import json
from datetime import timedelta, datetime

import aio_pika
import os
import dotenv
from pydantic import BaseModel, SecretStr

from trainings_app.auth.utils.jwt_utils import get_current_auth_user_with_role
from trainings_app.db.connection import AsyncpgPool
from trainings_app.repositories.clients import ClientRepository
from trainings_app.schemas.clients import ClientStatusEnum
from trainings_app.schemas.users import stuffer_roles, client_roles, GetUser, RoleEnum

dotenv.load_dotenv()


class RabbitMQSettings(BaseModel):
    MQ_USER: str
    MQ_PASSWORD: SecretStr
    MQ_HOST: str
    MQ_PORT: str

    @property
    def rabbit_mq_dsn(self) -> str:
        return f"amqp://{self.MQ_USER}:{self.MQ_PASSWORD.get_secret_value()}@{self.MQ_HOST}:{self.MQ_PORT}/"


rabbitmq_payment_settings = RabbitMQSettings(
    MQ_USER=os.getenv("PAYMENT_RABBITMQ_USER"),
    MQ_PASSWORD=SecretStr(os.getenv("PAYMENT_RABBITMQ_PASS")),
    MQ_HOST=os.getenv("PAYMENT_RABBITMQ_SERVER_IP"),
    MQ_PORT=os.getenv("PAYMENT_RABBITMQ_AMQP_PORT"),
)


def get_system_user() -> GetUser:
    return GetUser(
        id=1,
        username="SYSTEM",
        password_hash="SYSTEM",
        email="SYSTEM@example.com",
        role=RoleEnum.SYSTEM,
        created_at=datetime.utcnow()
    )


async def resolve_dependencies():
    pool = await AsyncpgPool.get_pool()
    conn = await pool.acquire()
    repo = ClientRepository(conn)
    user = get_system_user()
    return repo, user, conn


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        repo, user, conn = await resolve_dependencies()
        try:
            data = json.loads(message.body.decode())
            if data['status'] == 'PAID':
                client_record = await repo.update(
                    client_id=data['client_id'],
                    update_data={
                        'status': ClientStatusEnum.ACTIVE,
                        'expiration_date': datetime.fromisoformat(data['timestamp']) + timedelta(days=30),
                    },
                    user=user,
                )
                return client_record
        finally:
            await conn.close()


async def payment_consume():
    connection = await aio_pika.connect_robust(rabbitmq_payment_settings.rabbit_mq_dsn)
    channel = await connection.channel()
    payment_queue = await channel.declare_queue("payment_queue", durable=True)
    await payment_queue.consume(process_message)
    await asyncio.Future()
