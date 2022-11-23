from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.http import HttpRequest
from django.conf import settings

from ..magister import clear_session
from ..user.models import EUser
from .. import log

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

@receiver(user_logged_in)
def user_logged_in_callback(user: EUser, **kwargs):    
    log.info(f"user {user} logged in")

@receiver(user_logged_out)
def user_logged_out_callback(user: EUser, **kwargs): 
    log.info(f"user {user} logged out")
    clear_session()

def root_page(request):
    # if logged in: redirect to home page
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    # if not logged in: redirect to login page
    return redirect(settings.LOGIN_URL)