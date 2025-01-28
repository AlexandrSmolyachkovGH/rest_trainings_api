import logging
import os
import sys


def configure_logging(level: str = 'WARNING', console: bool = True, file: bool = False, file_name: str = 'app'):
    """
    Creates a logger with specific settings.
    """

    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    if level not in levels:
        raise ValueError(f"Invalid logger level: {level}")

    logger = logging.getLogger(file_name)
    logger.setLevel(levels.get(level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if file:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{file_name}.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not file and not console:
        logger.warning("No handlers specified. Logs will not be captured.")

    return logger


def check_logger(logger_level: str) -> bool:
    """
    Checks the validity of the logger level.
    """

    valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    return logger_level in valid_levels


def get_logger_level(env_var: str) -> str:
    """
    Gets the logger from the env file.
    In case of incorrect or missing values - returns default == 'ERROR'.
    """

    lvl = os.getenv(env_var, 'DEBUG')
    if not check_logger(lvl):
        print(f"Invalid log level '{lvl} in the env file. Defaulting to 'ERROR'")
        lvl = 'ERROR'
    return lvl
