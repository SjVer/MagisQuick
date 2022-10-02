from django.shortcuts import render
# from django import forms
from django.contrib.auth.forms import AuthenticationForm

# from src.user.models import EUser

class LoginForm(AuthenticationForm):
    pass

def login_view(request):
    print(request)
    return render(request, 'registration/login.html', {
		'form': LoginForm()
	})