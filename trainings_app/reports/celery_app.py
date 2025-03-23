from asgiref.sync import async_to_sync
import httpx
from datetime import timedelta, datetime, timezone
from celery import Celery, schedules

from trainings_app.settings import settings


app = Celery(
    'generate_report',
    broker=settings.rabbitmq_dsn,
    backend=None,
)


@app.task(queue='simple_report')
def create_simple_report():
    async_to_sync(_create_simple_report)()


async def _create_simple_report():
    today_utc = datetime.now(timezone.utc)
    yesterday_utc = today_utc - timedelta(days=3)

    get_url = "http://127.0.0.1:8000/users/for-report/"
    post_url = "http://127.0.0.1:8000/reports/"

    async with httpx.AsyncClient() as client:
        params = {
            "from_date": yesterday_utc.strftime('%Y-%m-%d'),
            "to_date": today_utc.strftime('%Y-%m-%d'),
        }
        get_response = await client.get(get_url, params=params)
        new_users = get_response.json()
        post_data = {
            'report_date_start': params["from_date"],
            'report_date_end': params["to_date"],
            'new_users': {'data': new_users}
        }
        response_post = await client.post(post_url, json=post_data)
        return response_post.json()


app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    "simple_report": {
        "task": 'trainings_app.reports.celery_app.create_simple_report',
        # "schedule": schedules.timedelta(seconds=30),
        "schedule": schedules.crontab(hour='8', minute='0'),
    },
}
