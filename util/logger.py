from loguru import logger
from config import LOG_FILE

log_file = LOG_FILE

logger.add(log_file, rotation="10MB", level="INFO", backtrace=True, diagnose=True)


def getLogger():
    return logger
