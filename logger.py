# imports
from datetime import datetime
import logging
from rich.logging import RichHandler

# logger instance
logger_data = logging.Logger(__name__)

# datetime for logging
dt = datetime.strftime(datetime.now(), '%Y%m%d-%H-%M-%S')

# define handlers
shell_handler = RichHandler()
file_handler_data = logging.FileHandler(f"logs/data/{dt}.log")

# formatters
shell_formatter = logging.Formatter('%(message)s')
file_formatter = logging.Formatter('%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s')

# set formatters
shell_handler.setFormatter(shell_formatter)
file_handler_data.setFormatter(file_formatter)

# set levels
logger_data.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler_data.setLevel(logging.DEBUG)

# add handlers
logger_data.addHandler(shell_handler)
logger_data.addHandler(file_handler_data)