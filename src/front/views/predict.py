from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from json import dumps

from .. import via_loading_page, with_error_message
from ...magister import get_session
from ... import figure_out

@login_required
@via_loading_page("Voorspel")
@with_error_message("De cijfers konden niet geladen worden.")
def predict_page(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	averages = figure_out.averages(session)

	json_averages = {}
	for s, g in averages.items(): json_averages[s] = dumps(g.__dict__)

	return render(request, "views/voorspel.html", {
		"settings": settings,
		"title": "Voorspel",
		"admin": session.user.is_superuser,
		"subjects": list(averages.keys()),
		"averages": json_averages,
	})