from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from .. import via_loading_page, with_error_message
from ...magister import get_session

@login_required
@via_loading_page("Cijfers")
@with_error_message("De cijfers konden niet geladen worden.")
def grades_page(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	return render(request, "views/grades.html", {
		"settings": settings,
		"title": "Cijfers",
	})