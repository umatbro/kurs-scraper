import sys
import logging
from selenium import webdriver
from scrapper import actions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run():
  logger.info('Executing')
  driver = webdriver.Firefox()
  ph = actions.PageHandler(driver)
  ph.login()
  # TODO Read slide content
  # ph.go_to_next_slide()
  