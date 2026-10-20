from __future__ import annotations

import logging
import sys
from pathlib import Path

LOG_DIR = Path.home() / "AppData" / "Local" / "HeartopiaTrainer" / "logs"


def setup_logging(verbose: bool = False) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / "trainer.log", encoding="utf-8"),
        ],
    )
    return logging.getLogger("heartopia_trainer")