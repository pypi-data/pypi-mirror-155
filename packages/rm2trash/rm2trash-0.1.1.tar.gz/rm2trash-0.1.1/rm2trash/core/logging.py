import sys
import logging


def get_logger():
    logger = logging.getLogger("RM2TRASH")
    if len(logger.handlers) == 0:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        console_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(console_handler)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] : %(message)s")
        console_handler.setFormatter(formatter)
    return logger


def set_level(level):
    if isinstance(level, str):
        get_logger().setLevel(level.upper())
    else:
        get_logger().setLevel(level)


debug = get_logger().debug
info = get_logger().info
warning = get_logger().warning
error = get_logger().error
fatal = get_logger().fatal
