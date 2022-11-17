from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from ..magister import get_session
from .. import figure_out

@login_required
def boeken_view(request: HttpRequest):
	session = get_session(request)
	session.require_userinfo()

	return render(request, "boeken.html", {
		"full_name": session.user.get_full_name(),
		"books": "</br>".join(figure_out.books(session)),
	})