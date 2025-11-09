import logging


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter that adds color to log messages based on their severity level
    and formats them with additional information such as timestamp, logger name, etc.
    """

    grey = "\x1b[38;20m"
    green = "\x1b[35;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d): %(debug_id)s "

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        """
        Format the specified log record as text.

        Args:
            record (LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        try:
            getattr(record, "debug_id")
            pass
        except:
            record.debug_id = ""
        return formatter.format(record)


# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure and add a console handler with the CustomFormatter
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)
