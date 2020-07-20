import logging
import sys

from pydantic import BaseSettings
from loguru import logger


class Settings(BaseSettings):
    amqp_broker_url: str = "amqp://guest:guest@localhost:5672/"
    mongodb_url: str = "mongodb://root:root@localhost:27017/"
    mongo_database: str = "IoTMiddleware"
    mongo_collection: str = "devices"
    log_level: str = "INFO"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def configure_logger(settings: Settings) -> None:
    intercept_handler = InterceptHandler()
    logging.root.setLevel(settings.log_level)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout}])
