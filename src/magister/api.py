from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from requests.cookies import RequestsCookieJar
from requests import get, Session
from os import system

from .. import log

__magister_cookies: RequestsCookieJar = None

def get_cookies():
    global __magister_cookies
    if __magister_cookies: return __magister_cookies

    s = Session()
    s.get("https://accounts.magister.net/")

    __magister_cookies = s.cookies
    log.debug(f"magister identities cookie: {s.cookies['Magister.Identities.XSRF'][:10]}...")
    return __magister_cookies

def search_tenants(request: HttpRequest):
    query = request.GET["query"]
    if len(query) < 3: return JsonResponse([], safe=False)

    try:
        r = get(
            f"https://accounts.magister.net/challenges/tenant/search?key={query}",
            cookies = get_cookies(),
            headers={
                "X-API-Client-ID": "EF15",
                "Content-Type": "application/json",
                "Host": "accounts.magister.net",
            }
        )
        r.raise_for_status()
        return JsonResponse(r.json() if r.content else [], safe=False)
        
    except Exception as e:
        log.error(f"failed to get schools ({e.__class__.__name__})")
        return JsonResponse([], safe=False)

def clear(request: HttpRequest):
    system("clear")
    return HttpResponseRedirect("/")