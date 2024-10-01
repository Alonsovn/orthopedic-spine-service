from src.utils.logUtil import log


def get_file_from_path(file_path):
    log.info("Getting file from path: %s", file_path)

    try:
        file = open(file_path, "rb")

        log.info("Completed getting file!")

        return file

    except Exception as e:
        log.exception(f"Failed getting file from {file_path}.Error: {e}")
