from datetime import datetime as dt
import termcolor as tc

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

LOG_FILE = "/dev/stdout" # "log.txt"

log_level = DEBUG

__log_file = open(LOG_FILE, "a")

def log(level, msg):
    if level > log_level: return

    level_string, color = [
        ("ERROR  ", "red"),
        ("WARNING", "yellow"),
        ("INFO   ", "cyan"),
        ("DEBUG  ", "green"),
    ][level]
    
    time = dt.now().strftime("%H:%M:%S")
    entry = tc.colored(f"[{level_string} - {time}] {msg}\n", color)
    
    __log_file.write(entry)
    __log_file.flush()
    
def error(msg):   log(ERROR, msg)
def warning(msg): log(WARNING, msg)
def info(msg):    log(INFO, msg)
def debug(msg):   log(DEBUG, msg)