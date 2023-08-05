# noinspection PyPackageRequirements
import __main__
import logging
import pathlib
import sys
import time
from types import MethodType

import logzero

from logzero import logger, ForegroundColors
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

logging.Formatter.converter = time.gmtime

SUCCESS = 25
VERBOSE = 15
TRACE = 5

DEFAULT_LEVEL = INFO
DEFAULT_MESSAGE_FORMAT = "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s"
DEFAULT_FILE_FORMAT = "[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_FILE_SIZE = 100 * 1024 * 1024
DEFAULT_BACKUP_COUNT = 5

DEFAULT_COLORS = {
    CRITICAL: ForegroundColors.RED,
    ERROR: ForegroundColors.RED,
    WARNING: ForegroundColors.YELLOW,
    SUCCESS: ForegroundColors.GREEN,
    INFO: ForegroundColors.GREEN,
    VERBOSE: ForegroundColors.BLUE,
    DEBUG: ForegroundColors.CYAN,
    TRACE: ForegroundColors.MAGENTA,
}


def add_logging_level(name: str, level: int) -> None:
    """Add a new logging level

    :param str name: Level name
    :param int level: Level severity
    """

    def _f(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    logging.addLevelName(level, name.upper())
    setattr(logging.Logger, name.lower(), _f)


add_logging_level("success", SUCCESS)
add_logging_level("verbose", VERBOSE)
add_logging_level("trace", TRACE)

logzero.loglevel(DEFAULT_LEVEL)
logzero.formatter(logzero.LogFormatter(fmt=DEFAULT_MESSAGE_FORMAT, datefmt=DEFAULT_DATE_FORMAT, colors=DEFAULT_COLORS))
path = pathlib.Path(__main__.__file__)
logzero.logfile(
    filename="_input_.log" if path.stem == "<input>" else path.with_suffix(".log"),
    formatter=logzero.LogFormatter(fmt=DEFAULT_FILE_FORMAT, datefmt=DEFAULT_DATE_FORMAT),
    maxBytes=DEFAULT_FILE_SIZE,
    backupCount=DEFAULT_BACKUP_COUNT,
    encoding="utf-8",
    loglevel=DEFAULT_LEVEL,
)


def _set_file(
    self,
    filename=None,
    formatter=None,
    mode="a",
    max_bytes=DEFAULT_FILE_SIZE,
    backup_count=DEFAULT_BACKUP_COUNT,
    encoding="utf-8",
    log_level=None,
    disable_stderr_logger=False,
):
    if filename is not None:
        formatter = formatter or logzero.LogFormatter(fmt=DEFAULT_FILE_FORMAT, datefmt=DEFAULT_DATE_FORMAT)
        log_level = log_level or self.level
    logzero.logfile(
        filename=filename,
        formatter=formatter,
        mode=mode,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
        loglevel=log_level,
        disableStderrLogger=disable_stderr_logger,
    )


logger.set_file = MethodType(_set_file, logger)
setattr(logger, "set_level", lambda level: logzero.loglevel(level))

logger.CRITICAL = CRITICAL
logger.ERROR    = ERROR
logger.WARNING  = WARNING
logger.INFO     = INFO
logger.DEBUG    = DEBUG
logger.SUCCESS  = SUCCESS
logger.VERBOSE  = VERBOSE
logger.TRACE    = TRACE

sys.excepthook = lambda e, v, tb: logger.critical(f"Uncaught Exception ➔ {e.__name__}: {v}", exc_info=(e, v, tb))
