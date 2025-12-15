import logging
from app.config import settings
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s [%(name)s] %(message)s",
    log_colors={
        "DEBUG": "purple",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
))

logging.root.handlers = [handler]
logging.root.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))