from datetime import datetime as dt
import termcolor as tc

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

log_level = DEBUG

def log(level, msg):
    if level > log_level: return

    level_string, color = [
        ("ERROR  ", "red"),
        ("WARNING", "yellow"),
        ("INFO   ", "cyan"),
        ("DEBUG  ", "green"),
    ][level]
    
    time = dt.now().strftime("%H:%M:%S")
    tc.cprint(f"[{level_string} - {time}] {msg}", color)
    
def error(msg):   log(ERROR, msg)
def warning(msg): log(WARNING, msg)
def info(msg):    log(INFO, msg)
def debug(msg):   log(DEBUG, msg)