import logging
import os
import datetime

def get_current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def create_log_folder():
    log_folder = os.path.join('logfiles', get_current_date())
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    return log_folder

log_folder = create_log_folder()
log_file = os.path.join(log_folder, 'log.txt')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)