import os
import sys
import logging
import logging.config
import traceback
from logging.handlers import TimedRotatingFileHandler

from icecream import install

from config.config import Config, load_config

# Install IceCream for debugging
install()

# Load configuration
config: Config = load_config()

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

# Define the log filename
filename = os.path.join(logs_dir, 'bot_logs.log')

# Set log level from config
LOG_LEVEL = config.logs_level
LOG_LEVEL = getattr(logging, LOG_LEVEL)

# Configure the logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Define the log format for the file handler
file_formatter = logging.Formatter('%(asctime)s | %(funcName)s | %(levelname)s | %(message)s',
                                   datefmt='%H:%M:%S')

# Set up a timed rotating file handler
log_file_handler = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1,
                                            encoding='utf-8', backupCount=50)
log_file_handler.suffix = "%d-%m-%Y"
log_file_handler.setFormatter(file_formatter)

# Add the file handler to the logger
logger.addHandler(log_file_handler)


def exception_handler(exc_type, exc_value, exc_traceback) -> None:
    """
    Exception handler to log tracebacks.

    Args:
        exc_type: The type of the exception.
        exc_value: The exception instance.
        exc_traceback: The traceback object.
    """
    if exc_type.__name__ == 'KeyboardInterrupt':
        return
    # Format the traceback into a string
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    # Log the formatted traceback
    logging.error('\n%s', tb_str)


# Set the custom exception handler
sys.excepthook = exception_handler
