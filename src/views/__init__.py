from django.shortcuts import render
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