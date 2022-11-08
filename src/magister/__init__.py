from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver

from dataclasses import dataclass
import requests, os

from .. import logging
from .ui import enter_credentails

__all__ = [
    "MagisterSession",
    "get_session",
    "get_grades"
]

@dataclass
class MagisterSession:
    tenant: str
    username: str
    access_token: str
    session_id: int
    person_id: int

def setup_driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # chrome_options.add_experimental_option("prefs", {
    #     "custom_handlers.registered_protocol_handlers": [
    #         {
    #             "default": True,
    #             "protocol": "m6loapp",
    #             "url": "https://google.com/%s"
    #         }
    #     ]
    # })
    
    chrome_driver = os.getcwd() + "/usr/bin/chromedriver"

    return webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path=chrome_driver
    )

def header(tenant, access_token):
    header = {
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }

    if tenant: header["Referer"] = f"https://{tenant}.magister.net/magister/"
    if access_token: header["Authorization"] = f"Bearer {access_token}"

    return header

def get_tenant(access_token):
    url = "https://magister.net/.well-known/host-meta.json"
    r = requests.get(url, headers=header(None, access_token), timeout=5)
    href = r.json()["links"][0]["href"]
    return href.lstrip("https://").split(".")[0]

def get_person_id(tenant, access_token):
    url = f"https://{tenant}.magister.net/api/toestemmingen"
    r = requests.get(url, headers=header(tenant, access_token), timeout=5)
    print(r.json())
    return int(r.json()["items"][0]["persoonId"])

def find_callback_response(responses):
    hiturl = f"https://accounts.magister.net/connect/authorize/callback"
    
    for request in responses:
        if hiturl in request.url:
            return request.response
            
    raise Exception("could not find authorization callback response")

def try_authenticate(school, username, passwd):
    logging.info(f"starting magister session")
    driver = setup_driver()

    driver.get(f"https://accounts.magister.net")
    logging.debug(f"retreiving accounts.magister.net")

    # enter credentials
    old_url = driver.current_url
    enter_credentails(driver, school, username, passwd)
    
    # wait for redirect
    logging.debug("waiting for redirect")
    WebDriverWait(driver, 5).until(EC.url_changes(old_url))
    responses = list(filter(lambda r: r.response, driver.requests))
    driver.quit()
    
    # extract information
    hiturl = f"https://accounts.magister.net/connect/authorize/callback"

    logging.debug("searching through responses")
    for request in responses:
        if hiturl in request.url:
            location = request.response.headers["location"]
            
            access_token = location.split("access_token=", 1)[1].split("&")[0]
            logging.debug(f"received token: {access_token[:5]}...{access_token[-5:]}")

            tenant = get_tenant(access_token)
            logging.debug(f"received tenant: {tenant}")

            person_id = get_person_id(tenant, access_token)
            logging.debug(f"received person_id: {person_id}")
            
            # pprint(
            #     # retreives list of school names
            #     requests.get(
            #         f"https://accounts.magister.net/challenges/tenant/search?key=CSG",
            #         headers=header(None, None)
            #     ).content
            # )
            
            logging.info("authentication complete")
            return MagisterSession(tenant, username, access_token, -1, person_id)
    
    raise Exception("could not find response")

# def get_grades(session: MagisterSession):
#     url = f"https://{session.school}.magister.net/api/personen/{session.id}/cijfers/laatste?top=25&skip=0"
#     r = requests.get(url, headers=header(session.school, session.token), timeout=5)
#     return r.json()

def get_session(tenant, username, passwd):
    try:
        return try_authenticate(tenant, username, passwd)
    except Exception as e:
        logging.error(f"failed to authenticate! (tenant: {tenant}, username: {username})")
        logging.error(f"{getattr(e, 'message', e)}")
