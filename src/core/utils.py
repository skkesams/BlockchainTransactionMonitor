from loguru import logger
import traceback
import yaml

import os

def log_exception(e, msg: str = None):
    logger.info(f"Error message: {e}")
    if msg:
        logger.info(msg)
    logger.info("-------------------------------Start Of Error Track Back-------------------------------\n")
    logger.info(str(traceback.format_exc()))
    logger.info(f"-------------------------------End Of Error Track Back---------------------------------")


def read_yaml(f="config.yaml"):
    if not os.path.exists(f):
        raise Exception(f"Path doesn't exists: {f}")
    with open(f, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
            return conf
        except yaml.YAMLError as exc:
            print(exc)
            raise exc