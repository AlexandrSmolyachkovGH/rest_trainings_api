from trainings_app.check_membership.celery_app import app

if __name__ == "__main__":
    app.worker_main([
        'worker',
        '--loglevel=info',
        '--pool=solo',
        '-Q',
        'check_membership_status',
    ])
