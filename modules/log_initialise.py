import logging
import os

def set_up_logging(dir_name:str, timestamp:str):
    """This will initialise the logger

    Args:
        dir_name (str): Directory name for where you want logs saved
        timestamp (str): Timestamp will be the name of the log file 
    """

    os.makedirs(dir_name, exist_ok=True)
    log_filename = f'{dir_name}/extract_log_{timestamp}.log'

    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO
    )

    return logging.getLogger()