from django.http import HttpRequest

from . import render_error

def errorcode_page(request, status, e, msg):
    if e: reason = e.__class__.__name__
    else: reason = None
    
    r = render_error(request, msg, reason)
    r.status_code = status
    return r

def error404_page(request: HttpRequest, *args, **kwargs):
    return errorcode_page(request, 404, None, "Deze pagina bestaat niet.")

def error500_page(request: HttpRequest, exception=None, *args, **kwargs):
    return errorcode_page(request, 500, exception, "Er is een interne fout opgetreden.")