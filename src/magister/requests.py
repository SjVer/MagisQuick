import requests

__all__ = [
    "get"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"

def get_header(tenant, access_token):
    header = {
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "nl-NL,nl;q=0.9,en-NL;q=0.8,en;q=0.7,en-US;q=0.6",
        "User-Agent": USER_AGENT
    }

    if tenant:
        header["Referer"] = f"https://{tenant}.magister.net/magister"
        header["Origin"] = f"https://{tenant}.magister.net"
    else:
        header["Referer"] = "https://accounts.magister.net/magister"
        header["Origin"] = "https://accounts.magister.net/"

    if access_token:
        header["Authorization"] = f"Bearer {access_token}"

    return header

def get(tenant, access_token, url):
    r = requests.get(
        url,
        headers=get_header(tenant, access_token),
        timeout=10
    )
    r.raise_for_status()
    return r