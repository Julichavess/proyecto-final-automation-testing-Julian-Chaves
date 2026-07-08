import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Un solo archivo de log por dia de ejecucion, para no perder historial entre corridas
_log_filename = datetime.now().strftime("%Y%m%d") + ".log"
_log_path = os.path.join(LOG_DIR, _log_filename)

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "qa_automation"):

    logger = logging.getLogger(name)

    if logger.handlers:
        # Ya esta configurado (por ejemplo si se llama varias veces en el mismo modulo)
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT)

    # Handler de archivo: guarda todo, util para depurar despues de una corrida
    file_handler = logging.FileHandler(_log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler de consola: solo lo importante, para no saturar la salida de pytest
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
