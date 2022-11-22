from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings

from ..magister.assets import loading_gif_url

def via_loading_page(title: str):
    def decorated(view_fn):
        def wrapped(request: HttpRequest):
            if "ViaLoadingPage" in request.headers.keys():
                return view_fn(request)
            else:
                return render(request, "load.html", {
                    "settings": settings,
                    "title": title,
                    "loading_gif_url": loading_gif_url(request.user.tenant)
                })
        return wrapped
    return decorated