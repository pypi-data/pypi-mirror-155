import logging
from commons.__init__ import log_dir
# from __init__ import log_dir
import os


def set_config(logger, logdir=""):
    if logdir != "":
        handler = logging.FileHandler(logdir)
    else:
        log_fdir = os.path.join(log_dir, 'bob.log')
        handler = logging.FileHandler(log_fdir)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger