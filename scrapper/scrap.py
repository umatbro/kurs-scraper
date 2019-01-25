import sys
import logging
from selenium import webdriver
from scrapper import actions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run():
  logger.info('Starting to scrap')
  driver = webdriver.Firefox()
  ph = actions.PageHandler(driver)
  ph.login()
  ph.read_and_save_slides(2)
