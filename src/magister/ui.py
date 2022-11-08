from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .. import logging

__all__ = ["enter_credentials"]

def wait_for_element(driver, id):
    locator = lambda d: d.find_element(value=id)
    return WebDriverWait(driver, 5).until(locator)

def enter_credentails(driver, school, username, passwd):
    # enter school
    elem = wait_for_element(driver, "scholenkiezer_value")
    logging.debug(f"entering school ({school})")
    elem.clear()
    elem.send_keys(school)
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_attribute(
            (By.CLASS_NAME, "input-drop-down-list-item"),
            "innerText", school
        )
    )
    elem.send_keys(Keys.RETURN)
    
    # enter username
    elem = wait_for_element(driver, "username")
    logging.debug(f"entering username ({username})")
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)

    # enter password
    elem = wait_for_element(driver, "rswp_password")
    logging.debug("entering password")
    elem.clear()
    elem.send_keys(passwd)
    elem.send_keys(Keys.RETURN)
