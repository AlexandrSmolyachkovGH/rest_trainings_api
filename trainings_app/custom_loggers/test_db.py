from trainings_app.custom_loggers.config import configure_logging, get_logger_level

logger_level = get_logger_level('TEST_DB_LOGGER')
test_db_logger = configure_logging(level=logger_level, console=False, file=True, file_name='test_db_logs')
