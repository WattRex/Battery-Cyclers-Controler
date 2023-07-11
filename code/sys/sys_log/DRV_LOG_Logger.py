import os
import logging
import logging.config

class DRV_LOG_Logger_c():
    def __init__(self, fileConfigPath:str):             #Example: fileConfigPath = './myLogginConfig.conf'
        if not os.path.exists('./log'):
            os.mkdir('./log')
        logging.config.fileConfig(fileConfigPath,disable_existing_loggers=True) #, encoding='utf-8'
        logging.debug('First log message')


class DRV_LOG_Custom_Formatter_c(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    #bold_red = '\x1b[31;1m'
    bold_red = '\x1b[1;37;41m'
    reset = '\x1b[0m'

    def __init__(self, fmt: str or None = ..., datefmt: str or None = ..., style = ...) -> None:
        super().__init__(fmt, datefmt, style)
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def DRV_LOG_LoggerGetModuleLogger(name:str):
    return logging.getLogger(name)