# data/logger.py

import logging
import os

def setup_logging(session_folder):
    log_file = os.path.join(session_folder, "session.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
