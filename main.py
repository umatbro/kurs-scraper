import logging
import os
import scrapper
from scrapper import scrap
import sys

BASE_DIR = (os.path.dirname(__file__))

if __name__ == '__main__':
  logger = logging.getLogger('scrapper')
  sh = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter('%(name)s: %(asctime)s %(name)s (%(funcName)s) :%(levelname)s: %(message)s')
  sh.setFormatter(formatter)
  logger.addHandler(sh)

  scrap.run()
