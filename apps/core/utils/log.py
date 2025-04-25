# pylint: disable=C0415,C0103,C0301
import logging

logger = logging.getLogger('cms')
logging_formats = {
    'simple': '%(asctime)s: %(levelname)s - %(message)s',
    'full': '%(asctime)s [%(name)s]: %(levelname)s - %(message)s (%(filename)s:%(funcName)s#%(lineno)d)'
}

class DBHandler(logging.Handler):
    def emit(self, record):
        from apps.core.models import Log

        payload = {
            'filename': record.filename,
            'function_name': record.funcName,
            'level_name': record.levelname,
            'level_number': record.levelno,
            'line_number': record.lineno,
            'module': record.module,
            'message': self.format(record),
            'path': record.pathname,
            'stack_info': record.stack_info,
            'args': record.args
        }
        Log.objects.create(**payload)


class ColoredFormatter(logging.Formatter):
    """Logging Formatter to add colors"""

    reset = "\x1b[0m"
    white = "\x1b[97;21m"
    red = "\x1b[91;21m"
    green = "\x1b[32;21m"
    bold_red = "\x1b[31;21m"
    blue = "\x1b[36;21m"
    yellow = "\x1b[33;21m"
    grey = "\x1b[37;21m"

    def format(self, record):
        FORMATS = {
            logging.DEBUG: self.green + str(self._fmt) + self.reset,
            logging.INFO: self.blue + str(self._fmt) + self.reset,
            logging.WARNING: self.yellow + str(self._fmt) + self.reset,
            logging.ERROR: self.red + str(self._fmt) + self.reset,
            logging.CRITICAL: self.bold_red + str(self._fmt) + self.reset
        }

        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
