import logging
import scrapper.config as cfg
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = cfg.get_config()

def login(driver: webdriver.Firefox):
  logout_page = config['webpage']['logout']
  logger.info(f'Opening {logout_page}')
  driver.get(logout_page)
  username_input = driver.find_element_by_id('username')
  password_input = driver.find_element_by_id('password')
  username_input.send_keys(config['credentials']['login'])
  password_input.send_keys(config['credentials']['password'])
  form = driver.find_element_by_tag_name('form')
  form.submit()

  # wait until trainer login is required
  WebDriverWait(driver, 10).until(lambda dr: dr.find_element_by_xpath("//*[contains(text(),'trener')]"), 'found form')

  # now find trainer credentials
  username_input = driver.find_element_by_id('username')
  password_input = driver.find_element_by_id('password')
  username_input.send_keys(config['trainer-credentials']['login'])
  password_input.send_keys(config['trainer-credentials']['password'])
  form = driver.find_element_by_tag_name('form')
  
  form.submit()

def go_to_next_slide(driver: webdriver.Firefox):
  time.sleep(3)
  logger.debug('Setting seconds to 0')
  driver.execute_script('console.log("xdd");')
  driver.execute_script('window.secs = 0; console.log(window.secs)')
  time.sleep(1)
  button_next = driver.find_element_by_id('btnDalej')
  logger.info('Clicking button next')

  button_next.click()
