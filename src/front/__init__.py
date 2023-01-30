from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings

from inspect import trace
from .. import log
from ..magister.session import NotAuthenticatedException

def root_page(request: HttpRequest):
    # if logged in: redirect to home page
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    # if not logged in: redirect to login page
    return redirect(settings.LOGIN_URL)

def render_error(request: HttpRequest, msg: str, reason: str | None):
    return render(request, "error.html", {
        "settings": settings,
        "title": "Error",
        "message": msg,
        "reason": reason,
	})

def error_page(request: HttpRequest, reason=None):
    return render_error(request, "Er is een onbekende fout opgetreden.", reason)

# decorators

def via_loading_page(title: str):
    def decorated(view_fn):
        def wrapped(request: HttpRequest):
            if "ViaLoadingPage" in request.headers.keys():
                return view_fn(request)
            else:
                return render(request, "load.html", {
                    "settings": settings,
                    "title": title,
                })
        return wrapped
    return decorated

def with_error_message(message: str):
    def decorated(view_fn):
        def wrapped(request: HttpRequest):
            try:
                return view_fn(request)
            except Exception as e:
                name = e.__class__.__name__
                log.error(f"an exception occurred: {name} ({e})")

                if e.__class__ == NotAuthenticatedException:
                    new_message = "Kon niet authenticeren met Magister."
                    return render_error(request, new_message, name)

                if settings.DEBUG:
                    f = trace()[-1]
                    log.error(f"{e}")
                    log.error(f"at {f.filename}")
                    log.error(f"{f.lineno}: `{f.code_context[0].strip()}`")
                return render_error(request, message, name)
        return wrapped
    return decorated
