from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

import os

from .. import logging

def setup_driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_driver = os.getcwd() + "/usr/bin/chromedriver"

    return webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path=chrome_driver
    )

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


def try_authenticate(tenant, username, passwd):
    driver = setup_driver()

    driver.get(f"https://{tenant}.magister.net")
    logging.debug(f"  retreiving {tenant}.magister.net")

    # enter credentials
    enter_credentails(driver, username, passwd)
    
    # wait for callback
    logging.debug("  waiting for callback")
    callback = driver.wait_for_request(
        "https://accounts.magister.net/connect/authorize/callback",
        5
    )
    driver.quit()
    
    # extract access token
    location = callback.response.headers["location"]
    access_token = location.split("access_token=", 1)[1].split("&", 1)[0]
    logging.debug(f"  access token: {access_token[:10]}...")

    return access_token

def authenticate(tenant, username, passwd):
    attempts = 3
    for a in range(attempts):
        try:
            logging.info(f"attempting magister authentication ({a+1}/{attempts})")
            return try_authenticate(tenant, username, passwd)
        except Exception as e:
            logging.error(f"failed to authenticate! (tenant: {tenant}, username: {username})")
            logging.error(f"{getattr(e, 'message', e)}")
            continue
    logging.error(f"too many retries ({attempts}/{attempts})")

