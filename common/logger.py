"""
日志配置
# common/logger.py

"""
import logging
import os
from datetime import datetime


def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
