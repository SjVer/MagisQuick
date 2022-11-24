from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings

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

def root_page(request):
    # if logged in: redirect to home page
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    # if not logged in: redirect to login page
    return redirect(settings.LOGIN_URL)

def render_error(request, msg):
    return render(request, "error.html", {
        "settings": settings,
        "title": "Error",
        "message": msg,
	})

def error_page(request):
    return render_error(request, "oeps")