import logging


class Logging:
    LEVEL = logging.INFO
    logger: logging.Logger = None

    @staticmethod
    def set_log_level(level):
        Logging.LEVEL = level
        Logging.logger = logging.getLogger("python-qa")
        Logging.logger.setLevel(level)


Logging.set_log_level(Logging.LEVEL)
