from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from datetime import datetime as dt

from .. import via_loading_page, with_error_message
from ...magister import get_session
from ... import figure_out

@login_required
@via_loading_page("Tijdlijn")
@with_error_message("De cijfers konden niet geladen worden.")
def timeline_page(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	grades = figure_out.grades(session)

	dates = []
	for _, gs in grades.items(): dates += [g.date for g in gs]
	dates = sorted(dates)
	fmtdate = lambda d: dt.fromisoformat(d).strftime("%-d %b. %Y")

	return render(request, "views/tijdlijn.html", {
		"settings": settings,
		"title": "Tijdlijn",
		"first_date": dates[0],
		"last_date": dates[-1],
		"first_date_f": fmtdate(dates[0]),
		"last_date_f": fmtdate(dates[-1]),
		"subjects": list(grades.keys()),
		"grades": grades,
	})