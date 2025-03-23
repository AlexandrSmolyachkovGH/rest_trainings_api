from trainings_app.custom_loggers.console_debug import console_logger
from trainings_app.reports.celery_app import app

if __name__ == "__main__":
    console_logger.info("[beat_report] Celery beat начал работу")
    app.start([
        "celery",
        "beat",
        "--loglevel=info",
    ])
