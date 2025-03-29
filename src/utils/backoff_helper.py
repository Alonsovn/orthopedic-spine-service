from src.utils.logUtil import log


def backoff_handler(details):
    log.info(f"Retrying due to an error: {details['exception']}")
