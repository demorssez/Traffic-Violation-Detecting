import sys
from loguru import logger

def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>',
        level = 'DEBUG'
    )

    logger.add(
        'logs/info.log',
        format = '{time:YYYY-MM-DD HH:mm:ss} | {file}:{line} | {level} | {message}',
        level = 'INFO',
        rotation = '10 MB',
        encoding = 'utf-8'
    )

    logger.add(
        'logs/violations.log',
        format = '{time:YYYY-MM-DD HH:mm:ss} | {message}',
        level = 'SUCCESS',
        filter = lambda record: record['level'].name == 'SUCCESS',
        rotation = '10 MB',
        encoding = 'utf-8'
    )
    
    return True
