from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

import os

from .. import logging
from .requests import get
from .ui import enter_credentails

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

def get_tenant(access_token):
    r = get(
        None, access_token,
        "https://magister.net/.well-known/host-meta.json",
    )
    href = r.json()["links"][0]["href"]
    return href.lstrip("https://").split(".")[0]

def get_person_id(tenant, access_token):
    # r = get(
    #     tenant, access_token,
    #     "https://accounts.magister.net/connect/userinfo",
    # )

    # print(r.text)

    # return int(r.json()["items"][0]["persoonId"])
    return -1

def try_authenticate(tenant, username, passwd):
    driver = setup_driver()

    driver.get(f"https://{tenant}.magister.net")
    logging.debug(f"  retreiving {tenant}.magister.net")

    # enter credentials
    old_url = driver.current_url
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
    logging.debug(f"  received access token: {access_token[:10]}...")

    # find login response and extract session id
    # response_url = find_response("/account/login", "login", responses)
    # session_id = response_url.split("sessionId=", 1)[1].split("&", 1)[0]
    session_id = "-------------------"
    logging.debug(f"  received session id: {session_id[:10]}...")

    # get person id
    person_id = get_person_id(tenant, access_token)
    logging.debug(f"  received person id: {person_id}")
    
    logging.info("authentication complete")
    return {
        "access_token": access_token,
        "session_id": session_id,
        "person_id": person_id
    }

def authenticate(tenant, username, passwd):
    attempts = 1
    for a in range(attempts):
        try:
            logging.info(f"attempting magister authentication ({a+1}/{attempts})")
            return try_authenticate(tenant, username, passwd)
        except Exception as e:
            logging.error(f"failed to authenticate! (tenant: {tenant}, username: {username})")
            logging.error(f"{getattr(e, 'message', e)}")
            continue
    logging.error(f"too many retries ({attempts}/{attempts})")
