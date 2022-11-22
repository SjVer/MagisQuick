# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
# from django.http import HttpRequest
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from ..magister import clear_session
from ..user.models import EUser
from .. import log

# class LoginForm(AuthenticationForm):
#     pass

# def login_view(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, 'login.html', {
#             'form': LoginForm()
#         })
#     else:
#         # method is "POST"
#         return redirect("/")
    
@receiver(user_logged_in)
def user_logged_in_callback(user: EUser, **kwargs):    
    log.info(f"user {user} logged in")

@receiver(user_logged_out)
def user_logged_out_callback(user: EUser, **kwargs): 
    log.info(f"user {user} logged out")
    clear_session()
    