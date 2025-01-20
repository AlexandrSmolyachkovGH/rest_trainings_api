import os

from trainings_app.logging.config import configure_logging, get_logger_level

logger_level = get_logger_level('REPO_LOGGER')
# logger_level = os.getenv('REPO_LOGGER') if os.getenv('REPO_LOGGER') else 'ERROR'
repo_logger = configure_logging(level=logger_level, console=True, file=True, file_name='repositories')
