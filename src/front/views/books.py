from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from datetime import datetime

from .. import via_loading_page, with_error_message
from ...magister import get_session
from ... import figure_out

@login_required
@via_loading_page("Boeken")
@with_error_message("De boeken konden niet geladen worden.")
def boeken_page(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	todays_subjects = figure_out.todays_subjects(session)
	upcoming_subjects = figure_out.upcoming_subjects(session)
	app_url_start = f"https://{session.user.tenant}.magister.net/magister/#/agenda/huiswerk/"

	return render(request, "views/boeken.html", {
		"settings": settings,
		"title": "Boeken",
		"full_name": session.user.get_full_name(),
		"date": datetime.today().strftime("%A %-d %B"),
		"app_url_start": app_url_start,
		"upcoming_subjects": upcoming_subjects,
		"todays_subjects": todays_subjects,
	})