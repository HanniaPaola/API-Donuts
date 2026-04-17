import logging
import os
import sys
from typing import Optional


def setup_logging(
    level: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    numeric = getattr(logging, lvl, logging.INFO)

    fmt = log_format or os.getenv(
        "LOG_FORMAT",
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    root = logging.getLogger()
    root.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))
    root.addHandler(handler)
    root.setLevel(numeric)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if numeric <= logging.DEBUG else logging.WARNING
    )
