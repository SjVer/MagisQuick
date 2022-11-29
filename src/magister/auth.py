from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from requests import get, post
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass

from .. import log

ISSUER = "https://accounts.magister.net"
SCOPES = ["openid", "profile", "offline_access"]
AUTH_CODE = "c0ad8cd4"
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

# get auth code
def get_code(tenant_id, username, password):
    auth_req = client.construct_AuthorizationRequest(request_args={
        "client_id": client.client_id,
        "response_type": "code id_token",
        "scope": SCOPES,
        "prompt": "select_account",
        **challenge_args
    })
    login_url = auth_req.request(client.authorization_endpoint)

    pre_auth_res = get(login_url, allow_redirects=False)
    auth_res = get(pre_auth_res.headers["location"], allow_redirects=False)
    auth_params = parse_qs(urlparse(auth_res.headers["location"]).query)
    session_id = auth_params["sessionId"][0]
    return_url = auth_params["returnUrl"][0]
    auth_cookies = auth_res.headers["Set-Cookie"]
    xsrf_token = auth_cookies.split("XSRF-TOKEN=", 1)[-1].split(";", 1)[0]

    def challenge(what, args):
        r = post(ISSUER + "/challenges/" + what,
            headers={
                "Content-Type": "application/json",
                "Cookie": auth_cookies,
                "X-XSRF-TOKEN": xsrf_token
            },
            json={
                "authCode": AUTH_CODE,
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
            log.error(f"failed to authenticate ({e.__class__.__name__})")
            return None

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
