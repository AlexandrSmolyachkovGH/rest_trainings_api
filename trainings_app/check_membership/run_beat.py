from trainings_app.check_membership.celery_app import app
from trainings_app.custom_loggers.console_debug import console_logger

if __name__ == "__main__":
    console_logger.info("[beat_check_membership] Celery beat начал работу")
    app.start([
        "celery",
        "beat",
        "--loglevel=info",
    ])
