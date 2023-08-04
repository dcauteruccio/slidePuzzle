import logging

logger = logging.getLogger('logger')
handler = logging.FileHandler('5001_puzzle.err')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

list = [1,2,3,4]

try:
    list[4]
except IndexError:
    logger.error("List Index out of Range")
