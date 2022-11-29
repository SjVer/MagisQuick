from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from django.forms import CharField, TextInput
from django.dispatch import receiver

from ..magister import clear_session
from ..user.models import EUser
from .. import log

class LoginForm(AuthenticationForm):

    school = CharField(
        widget=TextInput(attrs={
            "placeholder": "Je School",
            "list": "schools-list"
        }),
    )

    # TODO: school is an input field seperate form the form
    # instead, the js of the login page sets the school_id field
    # that is an invisible field of this form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {"placeholder": "Je Gebruikersnaam"}
        )
        self.fields['password'].widget.attrs.update(
            {"placeholder": "Je Wachtwoord"}
        )

    def clean(self):
        school = self.cleaned_data.get("school")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if school is not None and username is not None and password:
            self.user_cache = authenticate(
                self.request,
                school=school,
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


def login_page(request: HttpRequest) -> HttpResponse:
    return LoginView.as_view(
        template_name = "account/login.html",
        authentication_form=LoginForm
    )(request)

def logout_page(request: HttpRequest) -> HttpResponse:
    return LogoutView.as_view()(request)


@receiver(user_logged_in)
def user_logged_in_callback(user: EUser, **kwargs):    
    log.info(f"user {user} logged in")

@receiver(user_logged_out)
def user_logged_out_callback(user: EUser, **kwargs): 
    log.info(f"user {user} logged out")
    clear_session()
