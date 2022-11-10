from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from .. import logging

__all__ = ["enter_credentials"]

def wait_for_element(driver, id):
    locator = lambda d: d.find_element(value=id)
    return WebDriverWait(driver, 5).until(locator)

def enter_credentails(driver, username, passwd):
    # enter username
    elem = wait_for_element(driver, "username")
    logging.debug(f"  entering username ({username})")
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)

    # enter password
    elem = wait_for_element(driver, "rswp_password")
    logging.debug("  entering password")
    elem.clear()
    elem.send_keys(passwd)
    elem.send_keys(Keys.RETURN)
