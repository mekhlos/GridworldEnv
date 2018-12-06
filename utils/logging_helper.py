import os
import logging
import root_file

FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"


def create_log_dir(name):
    path = f'{root_file.ROOT_DIR}/logs/{name}/'

    if not os.path.exists(path):
        os.makedirs(path)


def get_logger(name):
    formatter = logging.Formatter(FORMAT)
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'{root_file.ROOT_DIR}/logs/{name}.log', mode='w')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger
