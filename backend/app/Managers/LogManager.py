import logging
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter


class LogManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager

        self.log_level = self.config_manager.log_level
        self.log_file = self.config_manager.log_file

        self.log = logging.getLogger("LogManager")

        file_handler = TimedRotatingFileHandler(
            filename=self.log_file,
            when='midnight',
            backupCount=7,
            encoding='utf-8'
        )

        file_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))

        self.log.addHandler(file_handler)

        if self.config_manager.debug:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(
                ColoredFormatter(
                    "%(white)s %(asctime)s :: %(log_color)s%(levelname)-8s%(reset)s%(blue)s%(message)s",
                    datefmt=None,
                    reset=True,
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white',
                    },
                    secondary_log_colors={},
                    style='%'
                )
            )

            self.log.addHandler(console_handler)

        self.log.setLevel(getattr(logging, self.log_level))

    def debug(self, string):
        self.log.debug(string)

    def info(self, string):
        self.log.info(string)

    def warning(self, string):
        self.log.warning(string)

    def error(self, string):
        self.log.error(string)

    def critical(self, string):
        self.log.critical(string)