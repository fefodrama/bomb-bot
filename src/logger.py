from src.date import dateFormatted

import telegram_send
import sys
import yaml


stream = open("./config.yaml", 'r')
c = yaml.safe_load(stream)

last_log_is_progress = False

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}

def logger(message, progress_indicator = False, color = 'default'):
    global last_log_is_progress
    color_formatted = COLOR.get(color.lower(), COLOR['default'])

    formatted_datetime = dateFormatted()
    formatted_message = "{} > {}".format(formatted_datetime, message)
    formatted_message_colored  = color_formatted + formatted_message + '\033[0m'

    
    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            formatted_message = color_formatted + "{} > {}".format(formatted_datetime, '⬆️ Processing last action..')
            sys.stdout.write(formatted_message)
            sys.stdout.flush()
        else:
            sys.stdout.write(color_formatted + '.')
            sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n')
        sys.stdout.flush()
        last_log_is_progress = False    

    print(formatted_message_colored)

    if (c['save_log_to_file'] == True):
        logger_file = open("./logs/logger.log", "a", encoding='utf-8')
        logger_file.write(formatted_message + '\n')
        logger_file.close()

    return True

def loggerMapClicked():
  logger('🗺️ New Map button clicked!')
  logger_file = open("./logs/new-map.log", "a", encoding='utf-8')
  logger_file.write(dateFormatted() + '\n')
  logger_file.close()

def sendTelegramLog(starttime):
    logger_file = open("./logs/logger.log", "r", encoding='utf-8')
    found = False
    text = ''
    for line in logger_file:
        if (starttime in line) or found:
            text = text + line
            found = True
    telegram_send.send(messages=[text])

def sendTelegramImg(image, text = None):
    with open(image, "rb") as image_d:
        if text is not None:
            telegram_send.send(messages=[text], images=[image_d])
        else:
            telegram_send.send(images=[image_d])
