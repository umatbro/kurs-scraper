import io
import os
import re
import logging
from typing import Union
import scrapper.config as cfg
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from main import BASE_DIR

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
  
  def _wait_for_slide_content_to_load(self) -> WebElement:
    """
    Wait for page to load and return slide content.

    :return: Web element holding slide content.
    """
    try:
      return WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.slajd_body')),
      )
    except TimeoutException as e:
      logger.error('Timeout when loading the slide')
      logger.exception(e)
      raise e

  def _next_button_is_present(self) -> Union[WebElement, None]:
    try:
      element = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.ID, 'btnDalej'))
      )
      logger.debug(f'Found button element: {element}')
      return element
    except TimeoutException:
      logger.info(f'Button \'Next\' was not found.')
      return None

  def click_next(self):
    self._wait_for_slide_content_to_load()
    self.driver.execute_script('window.secs = 0;')
    time.sleep(1)
    button_next = self.driver.find_element_by_id('btnDalej')
    button_next.click()

  def find_content_nodes(self):
    # wait for content to load
    slide_content = self._wait_for_slide_content_to_load()
    shown_nodes = self.driver.find_elements_by_css_selector('p.slajd_list')
    logger.debug(f'Length of shown nodes: {len(shown_nodes)}.')

    if len(shown_nodes) > 1:
      logger.warning(f'Length of shown nodes is longer than expected ({len(shown_nodes)}).')

    hidden_nodes = self.driver.find_elements_by_css_selector('p.slajd_list_hidden')
    logger.debug(f'Length of hidden nodes: {len(hidden_nodes)}.')
    
    while not all([element.is_displayed() for element in hidden_nodes]):
      logger.debug('Clicking next')
      self.click_next()

    logger.debug('All nodes should be visible')

  def reveal_hidden_text_by_clicking_next(self):
    self._wait_for_slide_content_to_load()
    shown_nodes = self.driver.find_elements_by_css_selector('p.slajd_list')
    logger.debug(f'Length of shown nodes: {len(shown_nodes)}.')

    if len(shown_nodes) > 1:
      logger.warning(f'Length of shown nodes is longer than expected ({len(shown_nodes)}).')

    hidden_nodes = self.driver.find_elements_by_css_selector('p.slajd_list_hidden')
    logger.debug(f'Length of hidden nodes: {len(hidden_nodes)}.')
    
    while not all([element.is_displayed() for element in hidden_nodes]):
      logger.debug('Clicking next')
      self.click_next()

    logger.debug('All nodes should be visible')

  def get_slide_element(self) -> WebElement:
    return self.driver.find_element_by_css_selector('td.slajd_body')

  def get_page_text(self) -> str:
    content = self.get_slide_element()
    return content.text

  def get_page_screenshot(self) -> io.BytesIO:
    content = self.get_slide_element()
    return content.screenshot_as_png

  def get_slide_name(self) -> str:
    elements = self.driver.find_elements_by_css_selector('div.nr_slajdu')
    text = ' '.join([el.text for el in elements]).replace('\n', ' ')
    if not re.match(r'^Blok: \d+\.\d+\. Godzina \d+ z \d+ nr slajdu: \d+$', text):
      logger.warning(f'Slide name does not match the pattern: {text}')
    return text

  def get_page_inner_html(self) -> str:
    return self.get_slide_element().get_attribute('innerHTML')

  def save_page_as_image(self, save_path='.', filename='default.png'):
    with open(os.path.join(save_path, filename), 'wb') as f:
      f.write(self.get_page_screenshot())

  def read_and_save_slides(self, number_of_slides=10, save_path=os.path.join(BASE_DIR, 'out.html')):
    logger.debug(f'save_path = {save_path}')
    with open(save_path, 'a+', encoding='utf-8') as f:
      for _ in range(number_of_slides):
        self.find_content_nodes()
        html = self.get_page_inner_html()
        slide_name = self.get_slide_name()
        logger.info(f'Saving slide {slide_name}')
        to_write = f'<article>\n<h3>{slide_name}</h3>\n{html}\n</article>\n'
        f.write(to_write)
        self.click_next()

  def read_and_save_pages_until_next_button_is_not_present(self, save_path=os.path.join(BASE_DIR, 'out.html')):
    self._wait_for_slide_content_to_load()
    with open(save_path, 'a+', encoding='utf-8') as f:
      while self._next_button_is_present():
        self.reveal_hidden_text_by_clicking_next()
        html = self.get_page_inner_html()
        slide_name = self.get_slide_name()
        logger.info(f'Saving slide {slide_name}')
        to_write = f'<article>\n<h3>{slide_name}</h3>\n{html}\n</article>\n'
        f.write(to_write)
        self.click_next()

  def close_browser(self):
    self.driver.close()
