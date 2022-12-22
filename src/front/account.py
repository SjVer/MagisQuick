from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.forms import CharField, TextInput
from django.dispatch import receiver

from ..magister import clear_session, get_session
from ..user.models import EUser
from .. import log

class LoginForm(AuthenticationForm):

    school = CharField(
        widget=TextInput(attrs={
            "placeholder": "Je School",
            "list": "schools-list",
            "class": "big_input",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                "class": "big_input",
                "placeholder": "Je Gebruikersnaam"
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                "class": "big_input",
                "placeholder": "Je Wachtwoord"
            }
        )

    def clean(self):
        clear_session()

        school = self.cleaned_data.get("school")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # if not api.school_is_valid(school):
        #     raise self.get_invalid_login_error()

        if school is not None and username is not None and password:
            self.user_cache = django_authenticate(
                self.request,
                school=school,
                username=username,
                password=password
            )
            if self.user_cache is None:
                e = self.get_invalid_login_error()
                self.add_error(None, e)
                raise e
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    return LoginView.as_view(
        template_name = "account/login.html",
        authentication_form = LoginForm
    )(request)

@login_required
def logout_page(request: HttpRequest) -> HttpResponse:
    get_session(request).end_session()
    return LogoutView.as_view()(request)

@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    log.info(f"deleting user {request.user}")
    request.user.delete()
    return HttpResponseRedirect("/logout")    

@receiver(user_logged_in)
def user_logged_in_callback(user: EUser, **kwargs):    
    log.info(f"user '{user}' logged in")

@receiver(user_logged_out)
def user_logged_out_callback(user: EUser, **kwargs): 
    log.info(f"user '{user}' logged out")
    clear_session()
