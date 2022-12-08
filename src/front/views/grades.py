from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from datetime import datetime as dt

from .. import via_loading_page, with_error_message
from ...magister import get_session
from ... import figure_out

@login_required
@via_loading_page("Cijfers")
@with_error_message("De cijfers konden niet geladen worden.")
def grades_page(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	averages = figure_out.averages(session)

	dates = []
	for _, gs in averages.items():
		dates += [g.date for g in gs]
	dates = sorted(dates)
	fmtdate = lambda d: dt.fromisoformat(d).strftime("%-d %b. %Y")

	return render(request, "views/grades.html", {
		"settings": settings,
		"title": "Cijfers",
		"first_date": fmtdate(dates[0]),
		"last_date": fmtdate(dates[-1]),
		"subjects": list(averages.keys()),
		"averages": averages,
	})