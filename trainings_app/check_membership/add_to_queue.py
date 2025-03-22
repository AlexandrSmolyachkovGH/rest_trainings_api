from trainings_app.check_membership.celery_app import check_membership_status

report_task = check_membership_status.apply_async(queue='check_membership_status')
print(f"Checking subscription statuses")
