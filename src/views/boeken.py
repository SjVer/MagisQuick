from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from . import via_loading_page
from ..magister import get_session
from .. import figure_out

@login_required
@via_loading_page("Boeken")
def boeken_view(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	return render(request, "views/boeken.html", {
		"settings": settings,
		"title": "Boeken",

		"full_name": session.user.get_full_name(),
		"books": "</br>".join(figure_out.books(session)),
	})