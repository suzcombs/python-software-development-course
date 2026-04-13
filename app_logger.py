"""
This module sets up logging for the application. Configures logging
"""
import logging


def setup_logging() -> None:
    """
    Sets up a logger for the application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',
        filemode='w'  # Overwrite log for each run - Remove if want to append
    )
