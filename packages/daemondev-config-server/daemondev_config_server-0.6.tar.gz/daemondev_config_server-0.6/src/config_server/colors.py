import logging

class Colors():
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    bgblack = "\x1b[40m"
    bgred = "\x1b[41m"
    bggreen = "\x1b[42m"
    bgyellow = "\x1b[43m"
    bgblue = "\x1b[44m"
    bgmagenta = "\x1b[45m"
    bgcyan = "\x1b[46m"
    bgwhite = "\x1b[47m"

    fgblack = "\x1b[30m"
    fgred = "\x1b[31m"
    fggreen = "\x1b[32m"
    fgyellow = "\x1b[33m"
    fgblue = "\x1b[34m"
    fgmagenta = "\x1b[35m"
    fgcyan = "\x1b[36m"
    fgwhite = "\x1b[37m"

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
