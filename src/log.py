from datetime import datetime as dt
from django.conf import settings
import termcolor as tc
from os import path, makedirs
from sys import stdout

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

LOG_FILE = f"logs/log-{dt.today().strftime('%d-%m-%Y')}.txt"

if settings.DEBUG:
    __log_level =  DEBUG
    __log_file = stdout
else:
    __log_level = eval(settings.LOG_LEVEL)
    if not path.exists(path.dirname(LOG_FILE)):
        makedirs(path.dirname(LOG_FILE))
    __log_file = open(LOG_FILE, "a")

__to_stdout = __log_file == stdout

def log(level, msg):
    if level > __log_level: return

    level_string, color = [
        ("ERROR  ", "red"),
        ("WARNING", "yellow"),
        ("INFO   ", "cyan"),
        ("DEBUG  ", "green"),
    ][level]
    
    time = dt.today().strftime("%H:%M:%S")
    if __to_stdout:
        entry = tc.colored(f"[{level_string} - {time}] {msg}\n", color)
    else:
        entry = f"[{level_string} - {time}] {msg}\n"
    
    __log_file.write(entry)
    __log_file.flush()
    
def error(msg):   log(ERROR, msg)
def warning(msg): log(WARNING, msg)
def info(msg):    log(INFO, msg)
def debug(msg):   log(DEBUG, msg)