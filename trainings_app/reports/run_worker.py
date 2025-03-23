from trainings_app.custom_loggers.console_debug import console_logger
from trainings_app.reports.celery_app import app

if __name__ == "__main__":
    console_logger.info("[worker_report] Celery worker начал работу")
    app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',
        '-Q',
        'simple_report',
    ])
