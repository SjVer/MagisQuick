from locale import setlocale, LC_TIME
from django import get_version
from datetime import datetime
from os import system
from . import log

system("clear")
setlocale(LC_TIME, "nl_NL.utf8")

log.info("=========== starting session ===========")
log.info(f"date: {datetime.now().strftime('%A %-d %B %Y')}")
log.info(f"django version: {get_version()}")
log.info(f"log file: {log.__log_file.name}")