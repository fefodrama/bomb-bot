import time

def dateFormatted(format = '%d/%m/%y %H:%M:%S'):
    datetime = time.localtime()
    formatted = time.strftime(format, datetime)
    return formatted