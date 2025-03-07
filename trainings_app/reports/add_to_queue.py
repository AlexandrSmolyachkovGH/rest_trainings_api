from trainings_app.reports.celery_app import create_simple_report

report_task = create_simple_report.apply_async(queue='simple_report')
print(f"Задача на генерацию отчета: {report_task.id}")
