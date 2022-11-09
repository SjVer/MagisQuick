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

def find_response(hiturl, name, responses):
    for url in responses:
        if hiturl in url:
            return url
            
    raise Exception(f"could not find authentication {name} response")

def try_authenticate(school, username, passwd):
    logging.info(f"attempting magister authentication")
    driver = setup_driver()

    driver.get(f"https://accounts.magister.net")
    logging.debug(f"retreiving accounts.magister.net")

    # enter credentials
    old_url = driver.current_url
    enter_credentails(driver, school, username, passwd)
    
    # wait for redirect
    logging.debug("waiting for redirect")
    WebDriverWait(driver, 5).until(EC.url_changes(old_url))
    driver.implicitly_wait(0.5)

    responses = [
        request.response.headers["location"] for request in
        list(filter(
            lambda r: r.response and r.response.headers["location"],
            driver.requests
        ))
    ]
    driver.quit()

    # find callback response and extract access token
    response_url = find_response(
        "https://accounts.magister.net/profile/oidc/redirect_callback",
        "redirect callback", responses
    )
    access_token = response_url.split("access_token=", 1)[1].split("&", 1)[0]
    logging.debug(f"received token: {access_token[:10]}...")

    # find login response and extract session id
    response_url = find_response("/account/login", "login", responses)
    session_id = response_url.split("sessionId=", 1)[1].split("&", 1)[0]
    logging.debug(f"received session id: {session_id[:10]}...")

    # get tenant and person id
    tenant = get_tenant(access_token)
    logging.debug(f"received tenant: {tenant}")

    person_id = get_person_id(tenant, access_token)
    logging.debug(f"received person id: {person_id}")
    
    # pprint(
    #     # retreives list of school names
    #     requests.get(
    #         f"https://accounts.magister.net/challenges/tenant/search?key=CSG",
    #         headers=header(None, None)
    #     ).content
    # )
    
    logging.info("authentication complete")
    return {
        "tenant": tenant,
        "username": username,
        "access_token": access_token,
        "session_id": session_id,
        "person_id": person_id
    }

def authenticate(school, username, passwd):
    for _ in range(2):
        try:
            return try_authenticate(school, username, passwd)
        except Exception as e:
            logging.error(f"failed to authenticate! (school: {school}, username: {username})")
            logging.error(f"{getattr(e, 'message', e)}")
            continue
    logging.error("too many retries")
