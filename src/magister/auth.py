from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oic import Client
from urllib.parse import parse_qs, urlparse
from requests import get, post
from django.core.cache import cache
from dataclasses import dataclass
from datetime import datetime as dt

from .. import log

ISSUER = "https://accounts.magister.net"
SCOPES = ["openid", "profile", "offline_access"]
ATTEMPTS = 3

class AuthError(Exception):
    pass

@dataclass
class TokenSet:
    access_token: str
    refresh_token: str
    id_token: str

# set up client
client = Client(client_authn_method=CLIENT_AUTHN_METHOD, client_id="M6LOAPP")
client.provider_config(ISSUER)
client.redirect_uris = ["m6loapp://oauth2redirect/"]
challenge_args, verifier = client.add_code_challenge()

def extract_param(url, param):
    return url.split(f"{param}=", 1)[1].split("&", 1)[0]

# Previous:
#   6-12-'22: `["2832a884","314d","201413","4161"],["2","3"]` -> "2014134161"
#   7-12-'22: 

def get_challenge_authcode(session_id, return_url):
    # try to use old code first
    if cache.get("challenge_auth_code_date") == dt.today().date():
        old_code = cache.get("challenge_auth_code")
        log.debug(f"  challenge auth code: {old_code} (cached)")
        return old_code

    # get html of login redirect page
    r = get(
        ISSUER + "/account/login",
        params={
            "sessionId": session_id,
            "returnUrl": return_url
        }
    )
    r.raise_for_status()
    
    # get js file
    js_file_id = r.text.split("src=\"js/account-", 1)[1].split(".js\"")[0]
    r = get(f"{ISSUER}/js/account-{js_file_id}.js")
    r.raise_for_status()

    # find relevant code
    js = r.text.split("r[zi[0]]=(o=", 1)[1].split(".map", 1)[0]
    split_index = js.find("],[") + 1

    # decrypt it
    strings = eval(js[:split_index])
    indices = [int(i) for i in eval(js[split_index + 1:])]
    auth_code = ''.join([strings[i] for i in indices])
    
    # store code to cache and return
    cache.set("challenge_auth_code", auth_code)
    cache.set("challenge_auth_code_date", dt.today().date()) 
    log.debug(f"  challenge auth code: {auth_code}")
    return auth_code

# get authentication code
def get_code(tenant_id, username, password):
    # notify magister that we'll be logging in
    login_url = client.construct_AuthorizationRequest(request_args={
        "client_id": client.client_id,
        "response_type": "code id_token",
        "scope": SCOPES,
        "prompt": "select_account",
        **challenge_args
    }).request(client.authorization_endpoint)
    pre_auth_res = get(login_url, allow_redirects=False)
    auth_res = get(pre_auth_res.headers["location"], allow_redirects=False)

    # extract the session-related information we need
    auth_params = parse_qs(urlparse(auth_res.headers["location"]).query)
    session_id = auth_params["sessionId"][0]
    return_url = auth_params["returnUrl"][0]
    auth_cookies = auth_res.headers["Set-Cookie"]
    xsrf_token = auth_cookies.split("XSRF-TOKEN=", 1)[-1].split(";", 1)[0]

    # get the challenge auth code
    challenge_auth_code = get_challenge_authcode(session_id, return_url)

    # send the challenges
    def challenge(what, args):
        r = post(ISSUER + "/challenges/" + what,
            headers={
                "Content-Type": "application/json",
                "Cookie": auth_cookies,
                "X-XSRF-TOKEN": xsrf_token
            },
            json={
                "authCode": challenge_auth_code,
                "sessionId": session_id,
                "returnUrl": return_url,
                **args
            }
        )
        r.raise_for_status()
        return r

    challenge("tenant", {"tenant": tenant_id})
    challenge("username", {"username": username})
    auth_cookies = \
        challenge("password", {"password": password}) \
        .headers["Set-Cookie"]

    # get the auth code
    auth_res = get(ISSUER + return_url, headers={"Cookie": auth_cookies}, allow_redirects=False)
    code = extract_param(auth_res.headers["location"], "code")
    
    return code

# get all tokens with the auth code
def get_tokenset(code):
    r = post(
        client.token_endpoint,
        data=f"grant_type=authorization_code&code={code}&code_verifier={verifier}" \
            "&redirect_uri=m6loapp%3A%2F%2Foauth2redirect%2F&client_id=M6LOAPP",
        headers={
            "X-API-Client-ID": "EF15",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "accounts.magister.net",
        }
    )
    r.raise_for_status()
    data = r.json()

    return TokenSet(
        data["access_token"],
        data["refresh_token"],
        data["id_token"]
    )

# get tokenset through a full authentication
def authenticate(tenant_id, username, password) -> TokenSet:
    for a in range(ATTEMPTS):
        try:
            log.info(f"attempting magister authentication ({a+1}/{ATTEMPTS})")
            code = get_code(tenant_id, username, password)
            log.debug(f"  authorization code: {code[:10]}...")
            return get_tokenset(code)
        except Exception as e:
            cache.delete("challenge_auth_code")
            log.error(f"failed to authenticate ({e.__class__.__name__})")

# get tokenset using refresh token
def refresh(refresh_token) -> TokenSet:
    try:
        r = post(
            client.token_endpoint,
            data=f"grant_type=refresh_token&refresh_token={refresh_token}&code_verifier={verifier}" \
                "&redirect_uri=m6loapp%3A%2F%2Foauth2redirect%2F&client_id=M6LOAPP",
            headers={
                "X-API-Client-ID": "EF15",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "accounts.magister.net",
            }
        )
        r.raise_for_status()
        data = r.json()

        return TokenSet(
            data["access_token"],
            data["refresh_token"],
            data["id_token"]
        )
    except Exception as e:
        log.warning(f"failed to refresh ({e.__class__.__name__})")
        return None

def end_session(id_token):
    try:
        r = get(
            client._endpoint("end_session_endpoint"),
            headers={
                "id_token_hint": id_token
            }
        )
        r.raise_for_status()
    except Exception as e:
        log.warning(f"failed to end session ({e.__class__.__name__})")