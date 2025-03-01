from trainings_app.custom_loggers.config import configure_logging, get_logger_level

logger_level = get_logger_level('REPO_LOGGER')
repo_logger = configure_logging(level=logger_level, console=True, file=True, file_name='repositories')
