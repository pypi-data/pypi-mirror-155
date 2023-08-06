import sys
import logging

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %("
    "message)s",
)


class MetaLogger(type):
    """
    Abstract base class for registering class inside unified logging system.
    """

    def __init__(cls, *args):
        super().__init__(*args)
        """
        Mangled name for unique identifier.
        """
        logger_attribute_name = "_" + cls.__name__ + "__logger"
        """
        Registering full inheritance pathname for logger.
        """
        logger_name = ".".join([c.__name__ for c in cls.mro()[-2::-1]])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))
