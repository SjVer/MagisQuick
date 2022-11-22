from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.conf import settings

from ..magister import get_session
from . import via_loading_page

@login_required
@via_loading_page("Account")
def account_view(request: HttpRequest):
	session = get_session(request)
	session.require_credentials()
	session.require_userinfo()
	
	return render(request, "views/account.html", {
		"settings": settings,
		"title": "Account",
		"user": session.user,
		"full_name": session.user.get_full_name()
	})