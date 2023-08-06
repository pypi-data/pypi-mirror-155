import logging
import os
from datetime import datetime


def logging_nemo_master(name: str):
    global logging_path
    if not os.path.exists(os.path.join(os.getcwd(), "Log Files")):
        os.makedirs(os.path.join(os.getcwd(), "Log Files"))
    logging_path = os.path.join(
        os.getcwd(),
        "Log Files",
        f"Log, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.log",
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logfile = logging.FileHandler(logging_path, mode="a")
    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s"))
    logger.addHandler(logfile)

    logstream = logging.StreamHandler()
    logstream.setLevel(logging.DEBUG)
    logstream.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s"))
    logger.addHandler(logstream)

    return logger


def logging_nemo_child(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logfile = logging.FileHandler(logging_path, mode="a")
    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s"))
    logger.addHandler(logfile)

    logstream = logging.StreamHandler()
    logstream.setLevel(logging.DEBUG)
    logstream.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s"))
    logger.addHandler(logstream)

    return logger
