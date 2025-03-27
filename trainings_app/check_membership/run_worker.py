from trainings_app.check_membership.celery_app import app
from trainings_app.custom_loggers.console_debug import console_logger

if __name__ == "__main__":
    console_logger.info("[worker_check_membership] Celery worker начал работу")
    app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',
        '-Q',
        'check_membership_status',
    ])
