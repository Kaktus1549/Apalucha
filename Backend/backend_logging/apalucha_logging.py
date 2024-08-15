import logging
import os
from time import mktime, sleep
from datetime import datetime
from werkzeug.serving import WSGIRequestHandler
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
load_dotenv()

webhook_url = os.getenv('DISCORD_WEBHOOK_URL', None)
webhook_logger = bool(os.getenv('WEBHOOK_LOGGER', False))
ballotbox_url = os.getenv('DISCORD_WEBHOOK_BALLOT_BOX', None)
ballotbox_logger = bool(os.getenv('WEBHOOK_BALLOT_BOX', False))

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
        
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
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
            self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
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

logger = logging.getLogger('apalucha_logger')
logger.setLevel(logging.DEBUG)
formatter = CustomFormatter()
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
daily_file_handler = DailyFileHandler(directory='./logs', encoding='utf-8')
daily_file_handler.setLevel(logging.DEBUG)
daily_file_handler.setFormatter(file_formatter)
logger.addHandler(daily_file_handler)

def ballot_box_log(level, message):
    if ballotbox_url:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time = f'[{time}]'
        if level == 'DEBUG':
            level_name = 'DEBUG'
        elif level == 'INFO':
            level_name = 'INFO'
        elif level == 'WARNING':
            level_name = 'WARNING'
        elif level == 'ERROR':
            level_name = 'ERROR'
        elif level == 'CRITICAL':
            level_name = 'CRITICAL'

        space_char = "\u200B "
        len_level = len(level_name)
        level_name = f'[{level_name}{" "*(8-len_level)}]'

        message = f'```\n{time} {level_name} {message}\n```'

        webhook = DiscordWebhook(url=ballotbox_url, content=message)
        response = webhook.execute()
        if response.status_code == 429:
            retry_after = response.json().get('retry_after', 1)  # default to 1 second if not specified
            sleep(int(retry_after))
            response = webhook.execute()

        if response.status_code != 200:
            # handle other errors if necessary
            error_message = f'Error sending message to Discord Webhook. Status code: {response.status_code}'
            formated = f'{time} {COLOR_RED}ERROR{COLOR_RESET}   {error_message}'
            logger.error(formated)
    else:
        logger.warning('Discord Ballotbox webhook URL not set')
def discord_log(level, message):
    if webhook_url:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time = f'[{time}]'
        if level == 'DEBUG':
            level_name = 'DEBUG'
        elif level == 'INFO':
            level_name = 'INFO'
        elif level == 'WARNING':
            level_name = 'WARNING'
        elif level == 'ERROR':
            level_name = 'ERROR'
        elif level == 'CRITICAL':
            level_name = 'CRITICAL'

        space_char = "\u200B "
        len_level = len(level_name)
        level_name = f'[{level_name}{" "*(8-len_level)}]'

        message = f'```\n{time} {level_name} {message}\n```'

        webhook = DiscordWebhook(url=webhook_url, content=message)
        response = webhook.execute()
        if response.status_code == 429:
            retry_after = response.json().get('retry_after', 1)  # default to 1 second if not specified
            sleep(int(retry_after))
            response = webhook.execute()

        if response.status_code != 200:
            # handle other errors if necessary
            error_message = f'Error sending message to Discord Webhook. Status code: {response.status_code}'
            formated = f'{time} {COLOR_RED}ERROR{COLOR_RESET}   {error_message}'
            logger.error(formated)
    else:
        logger.warning('Discord Webhook URL not set')
def log(level, message):
    if webhook_logger:
        discord_log(level, message)
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