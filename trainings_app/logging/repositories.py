from trainings_app.logging.config import configure_logging

repo_logger = configure_logging(level='ERROR', console=True, file=True, file_name='repositories')
