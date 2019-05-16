"""
    loggingsetup.py

    utility to set up logging
"""

import logging

APP_LOGNAME = "mail_forward"

def init_logging(loglevel=logging.DEBUG):
    """
        Creates standard logging for the logger_name passed in
    """
    logger = logging.getLogger(APP_LOGNAME)
    logger.setLevel(logging.DEBUG)
    channel = logging.StreamHandler()
    channel.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    channel.setFormatter(formatter)
    logger.addHandler(channel)
    logger.debug("Initialized logging")

    return logger
