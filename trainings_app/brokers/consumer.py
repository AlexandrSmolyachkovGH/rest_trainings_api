import asyncio
import json

import aio_pika
import os
import dotenv
from pydantic import BaseModel, SecretStr

from trainings_app.routers.payments import resolve_dependencies

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


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        repo, user, conn = await resolve_dependencies()
        try:
            data = json.loads(message.body.decode())
            p_id = data['payment_id']
            if data['status'] == 'PAID':
                record = await repo.get(p_id)
                record_dict = record.model_dump(exclude={"timestamp"})
                record_dict["payment_status"] = "PAID"
                update_record = await repo.update(p_id, record_dict)
                return update_record
        finally:
            await conn.close()


async def payment_consume():
    connection = await aio_pika.connect_robust(rabbitmq_payment_settings.rabbit_mq_dsn)
    channel = await connection.channel()
    payment_queue = await channel.declare_queue("payment_queue", durable=True)
    await payment_queue.consume(process_message)
    await asyncio.Future()
