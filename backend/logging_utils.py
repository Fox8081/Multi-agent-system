import logging
import sys

def setup_logger():
    """
    Sets up a logger to output to both a file (trace.log) and the console.
    """
    # I'm creating a logger named 'app_logger'.
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO) # Set the minimum level of messages to log.

    # This prevents adding multiple handlers if the function is called more than once.
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a formatter to define the structure of the log messages.
    # This format is clear and includes a timestamp, log level, and the message.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a handler to write logs to a file.
    file_handler = logging.FileHandler('trace.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a handler to also print logs to the console.
    # This is useful for debugging during development.
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

# Create a single logger instance to be used across the application.
app_logger = setup_logger()