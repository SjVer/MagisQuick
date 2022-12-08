from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from requests.cookies import RequestsCookieJar
from requests import get, Session
from os import system

from .. import log

class InvalidTenant(Exception): pass

__magister_cookies: RequestsCookieJar = None

def get_cookies():
    global __magister_cookies
    if __magister_cookies: return __magister_cookies

    s = Session()
    s.get("https://accounts.magister.net/")

    __magister_cookies = s.cookies
    log.debug(f"magister identities cookie: {s.cookies['Magister.Identities.XSRF'][:10]}...")
    return __magister_cookies

# In order to (for example) support the autocompletion of school names
# we need to be able to query the magister server for said names.
# This function does just that, but it first uses `get_cookies()` to
# get some cookies that magister wants.
def get_tenants(query):
    r = get(
        f"https://accounts.magister.net/challenges/tenant/search?key={query}",
        cookies = get_cookies(),
        headers={
            "X-API-Client-ID": "EF15",
            "Content-Type": "application/json",
            "Host": "accounts.magister.net",
        }
    )
    data = r.json() if (r and r.content) else []
    return data

# This function handles the `/api/search_tenants` request that just
# wraps around the function above. We only return the school's names
def search_tenants(request: HttpRequest):
    query = request.GET["query"]
    if len(query) < 3: return JsonResponse([], safe=False)

    try:
        data = get_tenants(query)
        names = [i["displayName"] for i in data]
        return JsonResponse(names, safe=False)
    except Exception as e:
        log.error(f"failed to get schools ({e.__class__.__name__})")
        return JsonResponse([], safe=False)

# Same as above, but searches for 1 school only and returns its ID
def get_tenant_id(name):
    data = get_tenants(name)
    if len(data) != 1 or data[0]["displayName"] != name:
        raise InvalidTenant
    return data[0]["id"]

# checks if a school name is valid
def school_is_valid(name):
    data = get_tenants(name)
    return len(data) == 1 and data[0]["displayName"] == name

# just clears the terminal, usefull for debugging
def clear(request: HttpRequest):
    system("clear")
    return HttpResponseRedirect("/")