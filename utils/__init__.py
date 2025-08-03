import logging

from utils.config import Config, parse_config_file

try:
    config = Config(**parse_config_file("config.ini"))
except Exception as e:
    logging.critical("Config not found!")