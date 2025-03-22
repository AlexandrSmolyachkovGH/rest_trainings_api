import json
from contextlib import asynccontextmanager

from asgiref.sync import async_to_sync
from datetime import datetime, timezone
from celery import Celery, schedules

from trainings_app.db.connection import AsyncpgPool
from trainings_app.reports.settings import conf_url
from trainings_app.schemas.clients import ClientStatusEnum as Statuses


@asynccontextmanager
async def get_conn():
    pool = await AsyncpgPool.get_pool()
    async with pool.acquire() as conn:
        await conn.set_type_codec(
            "json",
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        yield conn


app = Celery(
    'check_membership_status',
    broker=conf_url,
    backend=None,
)


@app.task(queue='check_membership_status')
def check_membership_status():
    async_to_sync(_check_membership_status)()


async def _check_membership_status():
    async with get_conn() as conn:
        today_utc = datetime.now(timezone.utc)
        update_query = f"""
            UPDATE clients
            SET status=$1
            WHERE status=$2 AND expiration_date>$3
            RETURNING id;
        """

        client_ids = await conn.fetch(update_query, Statuses.INACTIVE, Statuses.ACTIVE, today_utc)
        print(f"Num of updated statuses: {len(client_ids or [])}")
        return client_ids


app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    "check_membership": {
        "task": 'trainings_app.check_membership.check_membership_status',
        "schedule": schedules.crontab(hour='3', minute='0'),
    },
}
