from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from dataclasses import dataclass
from pprint import pprint
import requests
import os

@dataclass
class MagisterSession:
    school: str
    username: str
    token: str
    id: int

def setup_driver():
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_driver = os.getcwd() + "/usr/bin/chromedriver"

    return webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path=chrome_driver
    )

def wait_for_element(driver, id):
    locator = lambda d: d.find_element(value=id)
    return WebDriverWait(driver, 10).until(locator)

def header(school, token):
    return {
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://{school}.magister.net/magister/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }

def person_id(school, token):
    url = f"https://{school}.magister.net/api/toestemmingen"
    r = requests.get(url, headers=header(school, token), timeout=5)
    return int(r.json()["items"][0]["persoonId"])

def start_session(username, passwd, school):
    driver = setup_driver()
    driver.get(f"https://{school}.magister.net")
    print(f"opening {school}.magister.net...")

    # enter username
    elem = wait_for_element(driver, "username")
    print("entering username...")
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)

    # enter password
    old_url = driver.current_url
    elem = wait_for_element(driver, "rswp_password")
    print("entering password...")
    elem.clear()
    elem.send_keys(passwd)
    elem.send_keys(Keys.RETURN)
    
    # wait for redirect
    print("waiting for redirect...")
    WebDriverWait(driver, 5).until(EC.url_changes(old_url))
    responses = list(filter(lambda r: r.response, driver.requests))
    driver.quit()
    
    # extract access token
    hiturl = f"https://accounts.magister.net/connect/authorize/callback?client_id=M6-{school}.magister.net"

    print("searching through responses...")
    for request in responses:
        if hiturl in request.url:
            print("credentials found!")
            location = request.response.headers["location"]
            token = location.split("access_token=", 1)[1].split("&")[0]
            id = person_id(school, token)
            return MagisterSession(school, username, token, id)

def get_grades(session: MagisterSession):
    url = f"https://{session.school}.magister.net/api/personen/{session.id}/cijfers/laatste?top=25&skip=0"
    print(url)
    r = requests.get(url, headers=header(session.school, session.token), timeout=5)
    return r.json()




def test(username, passwd, school):
    import time

    import random
    import hashlib
    import base64
    verifier = ''.join(random.SystemRandom().choice("abcdef0123456789") for _ in range(128)) 
    state = ''.join(random.SystemRandom().choice("abcdef0123456789") for _ in range(32))
    nonce = ''.join(random.SystemRandom().choice("abcdefhijklmnopqrstuvwxyz") for _ in range(16))
    challenge = base64.urlsafe_b64encode(str(hashlib.sha256(verifier.encode("ascii"))).encode("ascii"))

    driver = setup_driver()
    driver.get(f"https://accounts.magister.net/connect/authorize?client_id=M6LOAPP&redirect_uri=m6loapp%3A%2F%2Foauth2redirect%2F&scope=openid%20profile%20offline_access%20magister.mobile%20magister.ecs&response_type=code%20id_token&state=${state}&nonce=${nonce}&code_challenge=${challenge}&code_challenge_method=S256&prompt=select_account")
    print(f"opening accounts.magister.net...")

    # enter school
    elem = wait_for_element(driver, "scholenkiezer_value")
    print("entering school...")
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
    print("entering username...")
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)

    # enter password
    elem = wait_for_element(driver, "rswp_password")
    print("entering password...")
    elem.clear()
    elem.send_keys(passwd)
    elem.send_keys(Keys.RETURN)
    
    # wait for redirect
    print("waiting for redirect...")
    # WebDriverWait(driver, 500).until(EC.url_changes(old_url))
    # responses = list(filter(lambda r: r.response, driver.requests))

    time.sleep(5)
    pprint(driver.window_handles)

    time.sleep(1000)

    driver.quit()

# session = start_session("22572", "Sj03rd@WvO.sv", "dewillem")
test("22572", "Sj03rd@WvO.sv", "CSG Willem van Oranje")
# pprint(get_grades(session))