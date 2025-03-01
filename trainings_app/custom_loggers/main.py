from trainings_app.custom_loggers.config import configure_logging, get_logger_level

logger_level = get_logger_level('MAIN_LOGGER')
main_logger = configure_logging(level=logger_level, console=False, file=True, file_name='main_logs')
