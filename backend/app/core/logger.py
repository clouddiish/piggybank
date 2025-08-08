import logging
from pathlib import Path

from app.core.config import get_settings


def get_logger(name: str = __name__) -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger(name)
    log_lvl_map = logging.getLevelNamesMapping()
    log_level = log_lvl_map[settings.log_level.value]

    logger.setLevel(log_level)

    formatter = logging.Formatter(settings.log_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    Path(settings.log_dir).mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(f"{settings.log_dir}/{settings.log_filename}")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
