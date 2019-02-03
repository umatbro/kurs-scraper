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
    # ph.get_valid_answers()
    ph.read_and_save_pages_until_next_button_is_not_present()
    logger.info('Finished logging')
