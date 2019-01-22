import logging
import os
from scrapper import scrap
import sys

logger = logging.getLogger('scrapper')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(name)s :%(levelname)s: %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)



# BASE_DIR = import os.path()

if __name__ == '__main__':
  scrap.run()