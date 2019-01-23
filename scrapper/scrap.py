import sys
import logging
from selenium import webdriver
from scrapper import actions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run():
  logger.info('Executing')
  driver = webdriver.Firefox()
  actions.login(driver)
  # TODO Read slide content
  # actions.go_to_next_slide(driver)