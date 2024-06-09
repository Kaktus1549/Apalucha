import logging
from datetime import datetime

#colors
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_ORANGE = '\033[33m'
COLOR_PURPLE = '\033[95m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'
COLOR_GREY = '\033[90m'

def log(level, message):
    timestamp = f"{COLOR_GREY}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLOR_RESET}"
    if level == "DEBUG" or level == "INFO":
        levelname_color = COLOR_GREEN
    if level == "WARNING":
        levelname_color = COLOR_YELLOW
    if level == "ERROR" or level == "CRITICAL":
        levelname_color = COLOR_RED
    levelname_formatted = f'{levelname_color}{level:<8}{COLOR_RESET}'
    formatted_message = f'{timestamp} {levelname_formatted} {message}'
    print(formatted_message)