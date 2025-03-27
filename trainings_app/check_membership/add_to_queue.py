from trainings_app.check_membership.celery_app import check_membership_status
from trainings_app.custom_loggers.console_debug import console_logger

report_task = check_membership_status.apply_async(queue='check_membership_status')
console_logger.info(f"Checking subscription statuses")
