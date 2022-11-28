from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from requests import get, Session
from os import system

from .. import log

__magister_cookies: str = None

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
    data = get(
        f"https://accounts.magister.net/challenges/tenant/search?key={query}",
        cookies = get_cookies()
    ).json()

    schools = [
        s["displayName"]
        for s in data
    ]
    return JsonResponse(schools, safe=False)

def clear(request: HttpRequest):
    system("clear")
    return HttpResponseRedirect("/")