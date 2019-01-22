"""
# Config template
webpage:
  login: https://login-webpage.address
  logout: https://logout-webpage.address

credentials:
  login: <login>
  password: <password>

trainer-credentials:
  login: <login>
  password: <password>
"""

import yaml
import logging

logger = logging.getLogger(__name__)

def get_config() -> dict:
  logger.debug('Opening config file')
  with open('config.yaml') as f:
    parsed = yaml.safe_load(f)
    logger.debug(f'Parsed content: {parsed}')
    return parsed

