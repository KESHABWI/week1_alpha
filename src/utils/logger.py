import logging
import sys 
from src.config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FMT

def get_logger(name:str) ->logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    logger.setlevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO ))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FMT))
    logger.addHandler(handler)
 
    logger.propagate = False
 
    return logger
 
 
def get_file_logger(name: str, filepath: str = "week1-ai-system.log") -> logging.Logger:
    logger = get_logger(name)
 
    has_file = any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    if not has_file:
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(
            logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FMT)
        )
        logger.addHandler(file_handler)
 
    return logger
 