import logging
import os
from datetime import datetime
from werkzeug.serving import WSGIRequestHandler

#colors
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_ORANGE = '\033[33m'
COLOR_PURPLE = '\033[95m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'
COLOR_GREY = '\033[90m'

class CustomFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = record.getMessage()
        
        if levelname == 'DEBUG':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'INFO':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'WARNING':
            levelname_color = COLOR_YELLOW
            message_color = COLOR_YELLOW
        elif levelname == 'ERROR':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        elif levelname == 'CRITICAL':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        else:
            levelname_color = ''
            message_color = ''
        
        timestamp = self.formatTime(record, self.datefmt)
        levelname_formatted = f'{levelname_color}{levelname:<8}{COLOR_RESET}'
        formatted_message = f'{COLOR_GREY}{timestamp} {levelname_formatted} {message_color}{message}{COLOR_RESET}'
        return formatted_message
class DailyFileHandler(logging.FileHandler):
    def __init__(self, directory, mode='a', encoding=None, delay=False):
        self.directory = directory
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.date_time = datetime.now().strftime("%Y-%m-%d")
        filename = self._get_filename()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)

    def _get_filename(self):
        return os.path.join(self.directory, f"{self.current_datetime}.log")

    def emit(self, record):
        new_datetime = datetime.now().strftime("%Y-%m-%d")
        if new_datetime != self.date_time:
            self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            self.date_time = new_datetime
            filename = self._get_filename()
            self.baseFilename = filename
            self.stream = self._open()
        super().emit(record)
class CustomRequestHandler(WSGIRequestHandler):
    def __init__(self, request, client_address, server, console_logger=None, file_logger=None):
        self.console_logger = console_logger
        self.file_logger = file_logger
        super().__init__(request, client_address, server)
    
    def log_request(self, code='-', size='-'):
        real_ip = self.headers.get('X-Real-IP')
        if not real_ip:
            real_ip = self.client_address[0]
        if self.console_logger:
            if code !='-':
                if str(code).startswith(('2', '3')):
                    code_message = f'{COLOR_GREEN}{code:<8}{COLOR_RESET}'
                elif str(code).startswith('4'):
                    code_message = f'{COLOR_ORANGE}{code:<8}{COLOR_RESET}'
                elif str(code).startswith('5'):
                    code_message = f'{COLOR_PURPLE}{code:<8}{COLOR_RESET}'
                else:
                    code_message = f'{code:<8}'
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f'{COLOR_GREY}{timestamp} {code_message} {self.requestline} from {real_ip} {COLOR_RESET}'
            if self.file_logger:
                uncolored_message = f'[{timestamp}] [{code:<8}] {self.requestline} from {real_ip}'
                self.file_logger.info(uncolored_message)
            self.console_logger.info(formatted_message)
        else:
            super().log_request(code, size)

def log(message, level, logger):
    if level == 'DEBUG':
        logger.debug(message)
    elif level == 'INFO':
        logger.info(message)
    elif level == 'WARNING':
        logger.warning(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'CRITICAL':
        logger.critical(message)
    else:
        logger.info(message)