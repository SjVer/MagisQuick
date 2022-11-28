from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from requests import get, post
from urllib.parse import parse_qs, urlparse

ISSUER = "https://accounts.magister.net"
AUTH_CODE = "bb6ebb6e"

client = Client(client_authn_method=CLIENT_AUTHN_METHOD, client_id="M6LOAPP")
client.provider_config(ISSUER)
challenge_args, verifier = client.add_code_challenge()

def get_code():
    client.redirect_uris = ["m6loapp://oauth2redirect/"]

    auth_req = client.construct_AuthorizationRequest(request_args={
        "client_id": client.client_id,
        "response_type": "code id_token",
        "scope": ["openid", "profile", "offline_access"],
        "prompt": "select_account",
        **challenge_args
    })
    login_url = auth_req.request(client.authorization_endpoint)

    auth_res = get(login_url, allow_redirects=False)
    auth_res = get(auth_res.headers["location"], allow_redirects=False)
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

    challenge("tenant", {"tenant": ...})
    challenge("username", {"username": ...})
    auth_cookies = challenge("password", {"password": ...}).headers["Set-Cookie"]

    auth_res = get(ISSUER + return_url, headers={"Cookie": auth_cookies}, allow_redirects=False)
    code = auth_res.headers["location"].split("#code=", 1)[1].split("&", 1)[0]
    
    return code

def get_token_set(code):
    r = post(
        client.token_endpoint,
        data=f"code={code}&redirect_uri=m6loapp%3A%2F%2Foauth2redirect%2F&client_id=M6LOAPP" \
             f"&grant_type=authorization_code&code_verifier={verifier}",
        headers={
            "X-API-Client-ID": "EF15",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "accounts.magister.net",
        }
    )
    r.raise_for_status()
    return r.json()

code = get_code()
print(get_token_set(code))

# TODO: we can get the access, id and refresh tokens now
#       what will we do with them?