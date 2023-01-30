from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.conf import settings

from ...magister import get_session

from .. import via_loading_page, with_error_message

@login_required
@via_loading_page("Instellingen")
@with_error_message("Instellingen konden niet geladen worden")
def settings_page(request: HttpRequest):
	session = get_session(request)
	
	return render(request, "views/instellingen.html", {
		"settings": settings,
		"title": "Instellingen",
		"admin": session.user.is_superuser,
	})