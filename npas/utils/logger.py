import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, level=logging.INFO, log_to_console=False):
    """Set up a logger with specified name, level, and console output option."""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if the logger already has handlers
    if not logger.handlers:
        # Create a rotating file handler
        handler = RotatingFileHandler(
            f"logs/{name}.log", 
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5  # Keep 5 backup files
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Optionally add console logging
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
    
    return logger
