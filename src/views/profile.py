from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.conf import settings

from ..magister import get_session

@login_required
def profile_view(request: HttpRequest):
	session = get_session(request)
	session.require_credentials()
	session.require_userinfo()
	
	return render(request, "views/profile.html", {
		"settings": settings,
		"title": "Account",
		"user": session.user,
		"full_name": session.user.get_full_name()
	})