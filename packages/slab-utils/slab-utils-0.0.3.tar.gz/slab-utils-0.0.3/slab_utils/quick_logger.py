"""
Quick Logger
"""

import logging


def get_stream_file_logger(
        logger_name=__name__, log_filename='runtime.log',
        file_output=True, steam_output=True
):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # File output
    if file_output:
        fileHandler = logging.FileHandler(log_filename, 'a', 'utf-8')
        fileHandler.setLevel(logging.DEBUG)
        formatter4File = logging.Formatter(
            '%(levelname)-8s - %(asctime)s(%(name)s):\n%(message)s',
            '%Y-%m-%d %H:%M:%S')
        fileHandler.setFormatter(formatter4File)
        logger.addHandler(fileHandler)

    # Console steam output
    if steam_output:
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        formatter4Stream = logging.Formatter(
            '%(asctime)s : %(message)s',
            '%H:%M:%S')
        streamHandler.setFormatter(formatter4Stream)
        logger.addHandler(streamHandler)

    return logger


logger = get_stream_file_logger()