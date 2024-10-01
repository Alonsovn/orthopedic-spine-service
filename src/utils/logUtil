import datetime
import logging

log = logging.getLogger(__name__)
DATE_FORMAT = "%m_%d_%Y"
date_now = datetime.datetime.now().strftime(DATE_FORMAT)

LOG_FILE_PATH = "./"


def file_logging_config():
    """Setup log format:\n <level> <time> - <message"""

    log_format = "%(levelname)s %(asctime)s - %(message)s "
    logging.basicConfig(filename=f"{LOG_FILE_PATH}app-logs-{date_now}.log", level=logging.INFO, format=log_format,
                        filemode="a")


def console_logging_config():
    """Setup log format:\n <level> <time> - <message"""

    log_format = "%(levelname)s %(asctime)s - %(message)s "
    logging.basicConfig(level=logging.INFO, format=log_format)
