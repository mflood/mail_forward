import logging
from mail_forward_flask.loggingsetup import init_logging

def test_global_init():
    init_logging(logging.DEBUG)

