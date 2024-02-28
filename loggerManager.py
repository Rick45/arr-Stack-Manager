#To use this, do logger = get_module_logger(__name__)
import logging


def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

#logger = get_module_logger(__name__)
#logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.warning("This is a warning message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")
# This will output:
# 2022-01-18 19:41:25,422 [__main__    ] DEBUG    This is a debug message
# 2022-01-18 19:41:25,422 [__main__    ] INFO     This is an info message
# 2022-01-18 19:41:25,422 [__main__    ] WARNING  This is a warning message
# 2022-01-18 19:41:25,422 [__main__    ] ERROR    This is an error message
# 2022-01-18 19:41:25,422 [__main__    ] CRITICAL This is a critical message