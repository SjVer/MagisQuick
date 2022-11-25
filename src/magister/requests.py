import requests

__all__ = [
    "get"
]

def get_header(tenant, access_token):
    header = {
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://accounts.magister.net"
    }

    if tenant: header["Referer"] = f"https://{tenant}.magister.net/magister/"
    if access_token: header["Authorization"] = f"Bearer {access_token}"

    return header

def get(tenant, access_token, url):
    r = requests.get(
        url,
        headers=get_header(tenant, access_token),
        timeout=5
    )
    r.raise_for_status()
    return r