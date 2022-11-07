from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass

def login_view(request):
    return render(request, 'login.html', {
		'form': LoginForm()
	})