import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from chatbot.config.settings import settings


def setup_logging() -> None:
    """Set up logging configuration for the chatbot application, 
    including file and console handlers with rotation. Logs are 
    stored in the path specified by settings.LOG_FILE_PATH, and 
    the log level is determined by settings.LOG_LEVEL."""
    
    log_path = Path(settings.LOG_FILE_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    root_logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5_242_880,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
