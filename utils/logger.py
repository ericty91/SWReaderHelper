import logging
from logging.handlers import RotatingFileHandler
def configure_logging():
 l=logging.getLogger("SW Reader Helper")
 if l.handlers:return l
 l.setLevel(logging.DEBUG);h=RotatingFileHandler("application.log",maxBytes=5000000,backupCount=5,encoding="utf-8");l.addHandler(h);return l
