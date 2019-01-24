import logging
import scrapper.config as cfg
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = cfg.get_config()


class PageHandler:
  def __init__(self, driver: webdriver.Firefox):
    self.driver = driver

  def login(self):
    logout_page = config['webpage']['logout']
    logger.info(f'Opening {logout_page}')
    self.driver.get(logout_page)
    username_input = self.driver.find_element_by_id('username')
    password_input = self.driver.find_element_by_id('password')
    username_input.send_keys(config['credentials']['login'])
    password_input.send_keys(config['credentials']['password'])
    form = self.driver.find_element_by_tag_name('form')
    form.submit()

    # wait until trainer login is required
    WebDriverWait(self.driver, 10).until(lambda dr: dr.find_element_by_xpath("//*[contains(text(),'trener')]"), 'found form')

    # now find trainer credentials
    username_input = self.driver.find_element_by_id('username')
    password_input = self.driver.find_element_by_id('password')
    username_input.send_keys(config['trainer-credentials']['login'])
    password_input.send_keys(config['trainer-credentials']['password'])
    form = self.driver.find_element_by_tag_name('form')
    
    form.submit()

  def go_to_next_slide(self):
    time.sleep(3)
    logger.debug('Setting seconds to 0')
    self.driver.execute_script('console.log("xdd");')
    self.driver.execute_script('window.secs = 0; console.log(window.secs)')
    time.sleep(1)
    button_next = self.driver.find_element_by_id('btnDalej')
    logger.info('Clicking button next')

    button_next.click()
