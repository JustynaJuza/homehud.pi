import logging

LOG_FORMAT = ' | %(asctime)s | [%(levelname)s] %(lineno)4s %(module)-30s | %(message)s'
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

logFormatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
rootLogger = logging.getLogger()

rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("homehudPi.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
