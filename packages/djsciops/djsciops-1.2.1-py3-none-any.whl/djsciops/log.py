import logging
import io
import sys
from . import settings as djsciops_settings

log = logging.getLogger("Primary")


class ConditionalFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, "disable_format") and record.disable_format:
            return record.getMessage()
        else:
            return logging.Formatter.format(self, record)


log_format = ConditionalFormatter(
    "[%(asctime)s][%(funcName)s][%(levelname)s]: %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)

log.setLevel(level=djsciops_settings.LOG_LEVEL.upper())
log.handlers = [stream_handler]


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    if log.getEffectiveLevel() == 10:
        log.debug("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    else:
        log.error(f"Uncaught exception: {exc_value}")


sys.excepthook = handle_exception


# https://github.com/tqdm/tqdm/issues/313#issuecomment-267959111
class TqdmToLogger(io.StringIO):
    """
    Output stream for TQDM which will output to logger module instead of
    the StdOut.
    """

    logger = None
    level = None
    buf = ""

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip("\r\n\t ")

    def flush(self):
        self.logger.log(self.level, self.buf)
