from datetime import datetime as dt

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

log_level = DEBUG

def log(level, *args, **kwargs):
    if level > log_level: return

    level_string = [
        "ERROR  ",
        "WARNING",
        "INFO   ",
        "DEBUG  ",
    ][level]
    
    time = dt.now().strftime("%H:%M:%S")
    print(f"[{level_string} - {time}] ", end="")
    print(*args, **kwargs)
    
def error(*args, **kwargs): log(ERROR, *args, **kwargs)
def warning(*args, **kwargs): log(WARNING, *args, **kwargs)
def info(*args, **kwargs): log(INFO, *args, **kwargs)
def debug(*args, **kwargs): log(DEBUG, *args, **kwargs)