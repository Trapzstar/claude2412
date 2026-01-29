"""
Centralized Logging System for SlideSense
Provides consistent logging across the application
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / f"slidesense_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Logger configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FORMAT_DETAILED = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logging.Logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        
        # Console Handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(console_formatter)
        
        # File Handler (DEBUG and above - more detailed)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT_DETAILED)
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger


# Module-level logger
logger = get_logger(__name__)


def log_info(message: str, **kwargs):
    """Log info message"""
    logger.info(message, **kwargs)


def log_debug(message: str, **kwargs):
    """Log debug message"""
    logger.debug(message, **kwargs)


def log_warning(message: str, **kwargs):
    """Log warning message"""
    logger.warning(message, **kwargs)


def log_error(message: str, **kwargs):
    """Log error message"""
    logger.error(message, **kwargs)


def log_critical(message: str, **kwargs):
    """Log critical message"""
    logger.critical(message, **kwargs)


if __name__ == "__main__":
    # Test logging
    logger = get_logger("slidesense.test")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
