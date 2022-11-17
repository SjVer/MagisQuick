from django.shortcuts import redirect
from django.conf import settings

def root_view(request):
    # if logged in: redirect to home page
    if request.user.is_authenticated:
        return redirect('/boeken/')

    # if not logged in: redirect to login page
    return redirect(settings.LOGIN_URL)